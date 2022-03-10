BOUNDARY_CONDITIONS = ("twisted", "periodic", "open")

TIGHT_BINDING_PARAMETER_DICT_TYPES = dict({"name": str,
                                           "L_x": int,
                                           "L_y": int,
                                           't': float,
                                           "BC_x": str,
                                           "BC_y": str})

TIGHT_BINDING_PARAMETER_DICT = dict({"name": "tight binding",
                                     "L_x": 5,
                                     "L_y": 6,
                                     't': 1.0,
                                     "BC_x": BOUNDARY_CONDITIONS,
                                     "BC_y": BOUNDARY_CONDITIONS,
                                     "types": TIGHT_BINDING_PARAMETER_DICT_TYPES})

TWO_BAND_ISOLATOR_PARAMETER_DICT_TYPES = dict({"name": str,
                                               "L_x": int,
                                               "L_y": int,
                                               't': float,
                                               "V_1": float,
                                               "V_2": float,
                                               "BC_x": str,
                                               "BC_y": str
                                               })

TWO_BAND_ISOLATOR_PARAMETER_DICT = dict({"name": "two band",
                                         "L_x": 5,
                                         "L_y": 6,
                                         't': 1.0,
                                         "V_1": 1.,
                                         "V_2": 2.,
                                         "BC_x": BOUNDARY_CONDITIONS,
                                         "BC_y": BOUNDARY_CONDITIONS,
                                         "types": TWO_BAND_ISOLATOR_PARAMETER_DICT_TYPES
                                         })

MODELS = dict({"tight binding": TIGHT_BINDING_PARAMETER_DICT,
               "two band": TWO_BAND_ISOLATOR_PARAMETER_DICT
               })

MODELS_TYPES = dict({"tight binding": TIGHT_BINDING_PARAMETER_DICT_TYPES,
                     "two band": TWO_BAND_ISOLATOR_PARAMETER_DICT_TYPES
                     })

LINEAR_PLOT_PARAMS = dict({"name": "linear",
                           "s_min": 0,
                           "s_max": 2,
                           "ds": 0.001,
                           "m_x": 1.,
                           "c_x": 0.,
                           "m_y": 0.5,
                           "c_y": 0,
                           "types": dict({"name": "linear",
                                          "s_min": float,
                                          "s_max": float,
                                          "ds": float,
                                          "m_x": float,
                                          "c_x": float,
                                          "m_y": float,
                                          "c_y": float})})

ELLIPSE_PLOT_PARAMS = dict({"name": "ellipse",
                            "s_min": 0,
                            "s_max": 1,
                            "ds": 0.001,
                            "a": 0.5,
                            "b": 0.2,
                            "x_0": 0.5,
                            "y_0": 0.5,
                            "types": dict({"name": str,
                                           "s_min": float,
                                           "s_max": float,
                                           "ds": float,
                                           "a": float,
                                           "b": float,
                                           "x_0": float,
                                           "y_0": float, })})

PLOTS = dict({"linear": LINEAR_PLOT_PARAMS,
              "ellipse": ELLIPSE_PLOT_PARAMS
              })

INDIVIDUAL_IMPURITY_PARAMETERS_DICT = dict({"x": 1,
                                            "y": 2,
                                            "energy": 2.,
                                            "types": dict({"x": int,
                                                           "y": int,
                                                           "energy": float})
                                            })

UNIFORM_IMPURITIES_PARAMETERS_DICT = dict({"N": 4,
                                           "a": -2.,
                                           "b": 2.,
                                           "types": dict({"N": int,
                                                          "a": float,
                                                          "b": float})
                                           })

IMPURITIES = dict({"uniform": UNIFORM_IMPURITIES_PARAMETERS_DICT,
                   "individual": INDIVIDUAL_IMPURITY_PARAMETERS_DICT
                   })
