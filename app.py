from flask import Flask, render_template, request, jsonify
 
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176b'

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/process', methods = ['POST'])
def process():
    #print('progress', request)+print 
    prevelanceType = request.form['prevType']
    prevelanceInput = request.form['prev']
    truePositive = request.form['truePos']
    falsePositive = request.form['falsePos']
    falseNegative = request.form['falseNeg']
    trueNegative = request.form['trueNeg']

    # remove string
    
    truePositive = eval(truePositive)
    falsePositive = eval(falsePositive)
    falseNegative = eval(falseNegative)
    trueNegative = eval(trueNegative)
    prevelanceType = eval(prevelanceType)
    prevelanceInput = eval(prevelanceInput)
#    print ('all args: %s' % request.form)
    
    # import packages
    
    from pba import cBox, computeConfidenceInterval, addIntervals, divideCbox, subtractIntervals, subtractNumberNcbox, subtractCboxNnumber, divideNumberNcbox, multiplyCboxNnumber, multiplyCbox, divideIntervals, addCboxNnumber
    # sensitivity
    sensitivity = computeConfidenceInterval(cBox(truePositive, addIntervals(truePositive, falseNegative)))
    # specificity
    specificity = computeConfidenceInterval(cBox(trueNegative, addIntervals(trueNegative, falsePositive)))
    # prevelence
    prevelance = computeConfidenceInterval(cBox(addIntervals(truePositive, falseNegative),
                                                addIntervals(addIntervals(truePositive, falseNegative),
                                                             addIntervals(falsePositive, trueNegative))))
    # positive predictive value
    ppv = computeConfidenceInterval(cBox(truePositive, addIntervals(truePositive, falsePositive)))
    # false positive rate
    fpr = computeConfidenceInterval(cBox(falsePositive, addIntervals(falsePositive, trueNegative)))
    # false negative rate
    fnr = computeConfidenceInterval(cBox(falseNegative, addIntervals(falseNegative, truePositive)))
    # negative predictive value
    npv = computeConfidenceInterval(cBox(trueNegative, addIntervals(trueNegative, falseNegative)))
    # positive likelihood ratio
    plr = computeConfidenceInterval(divideCbox(cBox(truePositive, addIntervals(truePositive, falseNegative)),
                     subtractNumberNcbox(1, cBox(trueNegative, addIntervals(trueNegative, falsePositive)))))
    # negative likelihood ratio
    nlr = computeConfidenceInterval(divideCbox(subtractNumberNcbox(1, cBox(truePositive, 
                                                addIntervals(truePositive, falseNegative))),
                                               cBox(trueNegative, addIntervals(trueNegative, falsePositive))))
    
    sens = cBox(truePositive, addIntervals(truePositive, falseNegative))   
    spec = cBox(trueNegative, addIntervals(trueNegative, falsePositive))
    
    if prevelanceType == 'cbox':
        prev = cBox(prevelanceInput[0], prevelanceInput[1])
        const = divideCbox(multiplyCbox(subtractCboxNnumber(divideNumberNcbox(1,
                prev), 1), subtractNumberNcbox(1, spec)), sens)
        ppv_new = divideNumberNcbox(1, addCboxNnumber(const, 1))
        ppv_new_interval = computeConfidenceInterval(ppv_new)
        const2 = divideCbox(multiplyCbox(subtractCboxNnumber(divideNumberNcbox(1,
                prev), 1), subtractNumberNcbox(1, sens)), spec)
        npv_new = divideNumberNcbox(1, addCboxNnumber(const2, 1))
        npv_new_interval = computeConfidenceInterval(npv_new)
        
        # ebc
        import numpy as np
        ppv_mean_lower = np.mean(ppv_new.get('lb'))
        ppv_mean_upper = np.mean(ppv_new.get('ub'))
        strip_area_ppv = ppv_new.get('ub') - ppv_new.get('lb')
        area_ppv = np.sum(strip_area_ppv) 
        n_param = 1/(area_ppv/len(ppv_new.get('lb')))-1
        k_param = (ppv_mean_lower + ppv_mean_upper)/2 * n_param
        
    elif prevelanceType == 'interval':
        
        prev = prevelanceInput
        const = divideCbox(multiplyCboxNnumber(subtractNumberNcbox(1, spec),
                subtractIntervals(divideIntervals([1, 1], prev), [1, 1])), sens)
        ppv_new = divideNumberNcbox(1, addCboxNnumber(const, 1))
        ppv_new_interval = computeConfidenceInterval(ppv_new)
        const1 = divideCbox(multiplyCboxNnumber(subtractNumberNcbox(1, sens),
                subtractIntervals(divideIntervals([1, 1], prev), [1, 1])), spec)
        npv_new = divideNumberNcbox(1, addCboxNnumber(const1, 1))
        npv_new_interval = computeConfidenceInterval(npv_new)
        
        # ebc
        import numpy as np
        ppv_mean_lower = np.mean(ppv_new.get('lb'))
        ppv_mean_upper = np.mean(ppv_new.get('ub'))
        strip_area_ppv = ppv_new.get('ub') - ppv_new.get('lb')
        area_ppv = np.sum(strip_area_ppv) * (ppv_new.get('support')[0][1]-ppv_new.get('support')[0][0])
        n_param = 1/(area_ppv)-1
        k_param = (ppv_mean_lower + ppv_mean_upper)/2 * n_param
        
    # Here I optimize to find the optimum value of k and n that corresponds to the ppv computed from the sensitivity,
    # specificity and prevelance. The problem has be formulated as an optimization problem:
    #                                min (errorArea^2)
    #                                such that: areaPbox <= areaCbox
    #                                 0<=k<=1000
    #                                 0<=n<=1000
    from scipy.optimize import minimize
    from numpy import array
    
    def objective(x):
        import numpy as np
        # pbox
        strip_area_ppv = abs(ppv_new.get('ub') - ppv_new.get('lb'))
        area_ppv = np.sum(strip_area_ppv)*(ppv_new.get('support')[0][1] - ppv_new.get('support')[0][0])
        # cbox
        k_para = x[0].tolist()
        n_para = x[1].tolist()
        Cbox = cBox(k_para, n_para)
        strip_area_cbox = abs(Cbox.get('ub') - Cbox.get('lb'))
        area_cbox = np.sum(strip_area_cbox) * (Cbox.get('support')[1] - Cbox.get('support')[0])
        return (area_cbox - area_ppv)**2
    
    def constraint(x):
        strip_area_ppv = abs(ppv_new.get('ub') - ppv_new.get('lb'))
        area_ppv = np.sum(strip_area_ppv)*(ppv_new.get('support')[0][1] - ppv_new.get('support')[0][0])
        # cbox
        k_para = x[0].tolist()
        n_para = x[1].tolist()
        Cbox = cBox(k_para, n_para)
        strip_area_cbox = abs(Cbox.get('ub') - Cbox.get('lb'))
        area_cbox = np.sum(strip_area_cbox) * (Cbox.get('support')[1] - Cbox.get('support')[0])
        return area_ppv - area_cbox
    
    b = (0, 2000)
    x0 = array([0, 1])
    bounds = (b, b)
    
    con = {'type':'ineq', 'fun': constraint}
    
    
    sol = minimize(objective, x0, method = 'SLSQP', bounds = bounds,
                   constraints = con, options = {'ftol': 1e-10, 'disp': True})
        
        

        
        
    # ppv    
    ppv_new_left_support = ppv_new.get('support')[0].tolist()
    ppv_new_right_support = ppv_new.get('support')[1].tolist()
    ppv_new_left_x = ppv_new.get('lb').tolist()
    ppv_new_right_x = ppv_new.get('ub').tolist()
    #npv
    npv_new_left_support = npv_new.get('support')[0].tolist()
    npv_new_right_support = npv_new.get('support')[1].tolist()
    npv_new_left_x = npv_new.get('lb').tolist()
    npv_new_right_x = npv_new.get('ub').tolist()
    k_param_opt = sol.x[0].tolist()
    n_param_opt = sol.x[1].tolist()
        
    return jsonify({'sensitivity_lower': sensitivity[0], 'sensitivity_upper': sensitivity[1],
                    'specificity_lower': specificity[0], 'specificity_upper': specificity[1],
                    'prevelance_lower': prevelance[0], 'prevelance_upper': prevelance[1],
                    'ppv_lower': ppv[0], 'ppv_upper':ppv[1],
                    'ppv_new_lower': ppv_new_interval[0], 'ppv_new_upper':ppv_new_interval[1],
                    'npv_new_lower': npv_new_interval[0], 'npv_new_upper':npv_new_interval[1],

                    'fpr_lower': fpr[0], 'fpr_upper': fpr[1],
                    'fnr_lower': fnr[0], 'fnr_upper': fnr[1],
                    'npv_lower': npv[0], 'npv_upper': npv[1],
                    'plr_lower': plr[0], 'plr_upper': plr[1],
                    'nlr_lower': nlr[0], 'nlr_upper': nlr[1],
                    'ppv_new_left_support': ppv_new_left_support,
                    'ppv_new_right_support': ppv_new_right_support,
                    'ppv_new_left_x': ppv_new_left_x,
                    'ppv_new_right_x': ppv_new_right_x,
                    'npv_new_left_support': npv_new_left_support,
                    'npv_new_right_support': npv_new_right_support,
                    'npv_new_left_x': npv_new_left_x,
                    'npv_new_right_x': npv_new_right_x,
                    'k_param': k_param, 'n_param': n_param,
                    'k_param_opt': k_param_opt, 'n_param_opt': n_param_opt
                    })

if __name__ == "__main__":
    app.run(debug = True)
    
                    