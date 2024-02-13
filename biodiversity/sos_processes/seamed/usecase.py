from sostrades_core.study_manager.study_manager import StudyManager

class Study(StudyManager):

    def __init__(self, execution_engine=None):
        super().__init__(__file__, execution_engine=execution_engine)

    def setup_usecase(self):

        dict_values = {
            f'{self.study_name}.seamed.Temperature': 15.3,
            f'{self.study_name}.seamed.Urbanisation':1.7*10**5,
            f'{self.study_name}.seamed.CO2_emissions':38000000000,
            f'{self.study_name}.seamed.energy_consumption':160000000000,
            f'{self.study_name}.seamed.Fishing_med': 1764*10**3,
            f'{self.study_name}.seamed.PlasticConsumption':53000000,
            f'{self.study_name}.seamed.PlasticNorms':0.5,
            f'{self.study_name}.seamed.ChemicalWaste':3145.6,
            f'{self.study_name}.seamed.Tourism':183,
            f'{self.study_name}.seamed.Renewal':300000, 
            }
        return dict_values


if '__main__' == __name__:
    uc_cls = Study()
    uc_cls.load_data()
    uc_cls.run(for_test=True)
    
