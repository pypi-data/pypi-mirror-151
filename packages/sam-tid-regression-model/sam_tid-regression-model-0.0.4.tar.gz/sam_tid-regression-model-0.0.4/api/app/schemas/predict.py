from typing import Any, List, Optional

from pydantic import BaseModel
from regression_model.processing.validation import SalesDataInputSchema


class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[float]]


class MultipleSalesDataInputs(BaseModel):
    inputs: List[SalesDataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        'date': '2021-11-10',
                        'feature_1': 1.9714,
                        'feature_2': 30.99,
                        'feature_3': 27.0,
                        'feature_4': 0.0,
                        'feature_5': 11.2857,
                        'feature_6': 16.0,
                        'feature_7': 1.105,
                        'feature_8': 29.7143,
                        'feature_9': 30.99,
                        'feature_10': 26.1135,
                        'feature_11': 27379.1909,
                        'feature_12': 28.3667,
                        'feature_13': 27869.5214,
                        'feature_14': 30.99,
                        'feature_15': 1.449,
                        'feature_16': 6.6053,
                        'feature_17': 30.99,
                        'feature_18': 1.0,
                        'feature_19': 1.0,
                        'feature_20': 30.99,
                        'feature_21': 30.99,
                        'feature_22': 29662.7762,
                        'feature_23': 68.6626,
                        'feature_24': 2.0,
                        'feature_25': 30.99,
                        'feature_26': 37.0,
                        'feature_27': 1.0,
                        'feature_28': 22216.2167,
                        'feature_29': 30.99,
                        'feature_30': 1.586,
                        'feature_31': 60.1477,
                        'feature_32': 25.2857,
                        'feature_33': 11.1429,
                        'feature_34': 27.1493,
                        'feature_35': 50319.25,
                        'feature_36': 27.5714,
                        'feature_37': 45.6976,
                        'feature_38': 1.0,
                        'feature_39': 1.0417,
                        'feature_40': 9.0,
                        'feature_41': 160432.8226,
                        'feature_42': 30739.3095,
                        'feature_43': 24.1429,
                        'feature_44': 0.9829,
                        'feature_45': 23.0,
                        'feature_46': 3.8338,
                        'feature_47': 1.916,
                        'feature_48': 273131.4524,
                        'feature_49': 0.5824,
                        'feature_50': 7.5333,
                        'feature_51': 2.5714,
                        'feature_52': 47.0,
                        'feature_53': 0.7985,
                        'feature_54': 97.1123,
                        'feature_55': 30.99,
                        'feature_56': 25.0,
                        'feature_57': 30978.5595,
                        'feature_58': 30.99,
                        'feature_59': 33.8571,
                        'feature_60': 1.0357,
                        'feature_61': 7.3457,
                        'feature_62': 30.99,
                        'feature_63': 1.0,
                        'feature_64': 5.0,
                        'feature_65': 30.99,
                        'feature_66': 28.1429,
                        'feature_67': 25047.881,
                        'feature_68': 30.99,
                        'feature_69': 26.8571,
                        'feature_70': 2.0,
                        'feature_71': 244645.1429,
                        'feature_72': 1.0,
                        'feature_73': 32042.7476,
                        'feature_74': 1.5234,
                        'feature_75': 26758.9609,
                        'feature_76': 17.9381,
                        'feature_77': 30.99,
                        'feature_78': 9.2373,
                        'feature_79': 30.99,
                        'feature_80': 57250.3946,
                        'feature_81': 1.2721,
                        'feature_82': 30.99,
                        'feature_83': 22.2903,
                        'feature_84': 96.8513,
                        'feature_85': 2.0,
                        'feature_86': 23.8058,
                        'feature_87': 49.0,
                        'feature_88': 67.0,
                        'feature_89': 104949.5357,
                        'feature_90': 30263.1028,
                        'feature_91': 4.9378,
                        'feature_92': 65.6412,
                        'feature_93': 1.1302,
                        'feature_94': 25.8333,
                        'feature_95': 26.0,
                        'feature_96': 2.0,
                        'feature_97': 51.0,
                        'feature_98': 59.5747,
                        'feature_99': 26.0,
                    }
                ]
            }
        }
