'''
Copyright 2022 Airbus SAS
Modifications on 2023/08/07-2023/11/03 Copyright 2023 Capgemini

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import pandas as pd

from climateeconomics.core.core_dice.macroeconomics_model import MacroEconomics
from climateeconomics.glossarycore import GlossaryCore
from sostrades_core.execution_engine.sos_wrapp import SoSWrapp
from sostrades_core.tools.post_processing.charts.chart_filter import ChartFilter
from sostrades_core.tools.post_processing.charts.two_axes_instanciated_chart import InstanciatedSeries, \
    TwoAxesInstanciatedChart


class MerMediteranne(SoSWrapp):
    # ontology information
    _ontology_data = {
        'label': 'Mer Mediteranne Model',
        'type': 'Research',
        'source': 'SoSTrades Project',
        'validated': '',
        'last_modification_date': '',
        'category': '',
        'definition': '',
        'icon': '',
        'version': '',
    }
    _maturity = 'Research'
    DESC_IN = {'Temperature': {'type': 'float', 'unit': '°C'},
        'CO2': {'type': 'float', 'unit': '-'},
        'FishConsumption' : {'type': 'float', 'unit': '-'},
        'EnergyOffshore' : {'type': 'float', 'unit': '-'}, #prendre totalenergy
        'Sand' : {'type': 'float', 'unit': 't'}, #exist or only urbanisation/construction ?
    	'PlasticConsumption' : {'type': 'float', 'unit': 't'}, #from economy ? or directly plastic in oceans ??
    	'PlasticNorms' : {'type': 'float', 'unit': '%'}, #% of untreated waste ->for economic impact ?
    	'ChemicalWaste' : {'type': 'float', 'unit': '-'}, #metals and chemical pollution
    	'Tourism' : {'type': 'float', 'unit': 'people'} #à tirer de la population ?
    }

    DESC_OUT = {
        'Health': {'type': 'float', 'unit': '-'},
        "Cost" : {'type': 'float', 'unit': 'M€'},
        "BioLoss": {'type': 'float', 'unit': '%'}
    }

    def run(self):
        #five main causes of biodiversity loss
        TBD = 1 #coefficients to determine

        #Pollution
        PlasticConsumption = self.get_sosdisc_inputs('PlasticConsumption')
        PlasticNorms = self.get_sosdisc_inputs('PlasticNorms')
        ChemicalWaste = self.get_sosdisc_inputs('ChemicalWaste') #affect the same species than plastic but combined effects
        Tourism = self.get_sosdisc_inputs('Tourism')
        plastic = (PlasticConsumption * PlasticNorms) * (1.4 * Tourism) #current tourism = +40% plastic pollution

        #Invasive Species
        newspecies = 0.5 * TBD *plastic + TBD * (fishing + Tourism)
        #plastifere = new species travelling fast but only viruses and bacterias, half very dangerous

        # Climate
        Temperature = self.get_sosdisc_inputs('Temperature')
        CO2 = self.get_sosdisc_inputs('CO2')
        pH = 0.3 * TBD * CO2 - TBD * plastic #CO2 absorbtion and plastic dissolution are the main factor for acidification
        #30% CO2 dans océan, pour le moment on fait -0.001 par an environ donc retro engineer / idem pour plastique auj à -0.005 dans zones très polluées 

        #Overexploitation
        FishConsumption = self.get_sosdisc_inputs('FishConsumption')
        Health = TBD * plastic + TBD * ChemicalWaste
        if Health < ...: #si trop pollué alors non comestible ou alors nettement moins d'espèces 
            fishing = TBD * FishConsumption
        else :
            fishing = TBD * FishConsumption/TBD #diviser par 10 ??
            #mettre aussi max pour éviter surpêche (on va pêcher ailleurs ?)

        #Destruction of habitats
        offshore = self.get_sosdisc_inputs('EnergyOffshore')
        sand = self.get_sosdisc_inputs('Sand') #ou alors extraire de urbanisation/indsutrie pour calculer les besoins en sable ?

        #Biodiversity loss, % of species of danger due to each factor
        # numbers are still approximations
        BioLoss = 0.6 * Temperature + 0.2 * pH + 0.2 * (plastic + ChemicalWaste) + 0.1 * newspecies + TBD * fishing + TBD * offshore + TBD * sand
    
        #cost of pollution, norms... and benefits of fishing, tourism, offshore...
        Cost = 13 * plastic + 1 * PlasticNorms - TBD * fishing - TBD*Tourism - TBD * offshore - TBD * sand + TBD * Health

        outputs_dict = {
            
        }

        #-- store outputs
        self.store_sos_outputs_values(outputs_dict)
