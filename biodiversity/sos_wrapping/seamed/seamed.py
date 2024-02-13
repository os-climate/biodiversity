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
from sostrades_core.execution_engine.sos_wrapp import SoSWrapp
from sostrades_core.tools.post_processing.charts.chart_filter import ChartFilter
from sostrades_core.tools.post_processing.charts.two_axes_instanciated_chart import InstanciatedSeries, \
    TwoAxesInstanciatedChart


class Seamed_model(SoSWrapp):
    # ontology information
    _ontology_data = {
        'label': 'Seamed_model',
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
    DESC_IN = {'Temperature': {'type': 'float', 'unit': 'Â°C'},
        'CO2_emissions': {'type': 'float', 'unit': 't'},
        'Fishing_med' : {'type': 'float', 'unit': 't'},
        'energy_consumption' : {'type': 'float', 'unit': '-'}, #prendre totalenergy
        'Urbanisation' : {'type': 'float', 'unit': 'kmÂ²'}, 
    	'PlasticConsumption' : {'type': 'float', 'unit': 't'},
    	'PlasticNorms' : {'type': 'float', 'unit': '%'}, #% of untreated waste ->for economic impact ?
    	'ChemicalWaste' : {'type': 'float', 'unit': 't'}, #metals and chemical pollution
    	'Tourism' : {'type': 'float', 'unit': 'people'}, #Ã  tirer de la population ?
        'Renewal' : {'type': 'float', 'unit': 'fish'}
    }

    DESC_OUT = {
        'Health': {'type': 'float', 'unit': '-'},
        "Cost" : {'type': 'float', 'unit': 'Mâ‚¬'},
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

         #Overexploitation
        FishConsumption = self.get_sosdisc_inputs('Fishing_med')
        Renewal = self.get_sosdisc_inputs('Renewal')
        FishHealth = TBD * plastic + TBD * ChemicalWaste
        if FishHealth < TBD : #si trop polluÃ© alors non comestible ou alors nettement moins d'espÃ¨ces 
            fishing = TBD * FishConsumption - Renewal
            Health = FishHealth 
        else :
            fishing = TBD * FishConsumption/10 #diviser par 10 ??
            Health=0
            #mettre aussi max pour Ã©viter surpÃªche (on va pÃªcher ailleurs ?)
        #Invasive Species
        newspecies = 0.08*(0.5*(fishing+Tourism)+0.13*plastic)
        #plastifere = new species travelling fast but only viruses and bacterias, half very dangerous

        # Climate
        Temperature = self.get_sosdisc_inputs('Temperature')
        CO2 = self.get_sosdisc_inputs('CO2_emissions')
        pH = -3e-12 *(CO2+plastic)
        #plastic dissolution emits CO2 so same effect on acidification

       

        #Destruction of habitats
        energy = self.get_sosdisc_inputs('energy_consumption')
        Urbanisation = self.get_sosdisc_inputs('Urbanisation') 
        sand = TBD * Urbanisation
        offshore = energy * TBD

        #Biodiversity loss, % of species of danger due to each factor
        # numbers are still approximations
        BioLoss = 0.6 * Temperature + (0.4 *pH +1) + 0.2 * (plastic + ChemicalWaste) + 0.1 * newspecies + TBD * fishing + TBD * offshore + TBD * sand
    
        #cost of pollution, norms... and benefits of fishing, tourism, offshore...
        Cost = 13 * plastic + 1 * PlasticNorms - TBD * fishing - TBD*Tourism - TBD * offshore - TBD * sand

        outputs_dict = {
            'Health': Health,
            "Cost" : Cost,
            "BioLoss": BioLoss
        }

        print(BioLoss)
        #store outputs
        self.store_sos_outputs_values(outputs_dict)


    def get_chart_filter_list(self):

        # For the outputs, making a graph for tco vs year for each range and for specific
        # value of ToT with a shift of five year between then

        chart_filters = []

        chart_list = ['BioLoss', 'Cost','Health']
        # First filter to deal with the view : program or actor
        chart_filters.append(ChartFilter(
            'Charts', chart_list, chart_list, 'charts'))

        return chart_filters 

    def bioloss_evolution(BioLoss_data, instanciated_charts):
        co2 = self.get_sosdisc_inputs('CO2_emissions')
        # Chart name
        chart_name = 'BioLoss Evolution over CO2 Levels'
        # Initialize new chart
        new_chart = TwoAxesInstanciatedChart('CO2 Levels', 'BioLoss', chart_name=chart_name)
        # Create series for BioLoss data over CO2 levels
        new_series = InstanciatedSeries(co2, BioLoss_data, 'BioLoss', 'lines')
        # Append series to chart
        new_chart.series.append(new_series)
        # Append chart to instanciated_charts
        instanciated_charts.append(new_chart)
        return instanciated_charts
    
    def health_evolution(health_data, instanciated_charts):
        co2 = self.get_sosdisc_inputs('CO2_emissions')
    
        chart_name = 'Health Evolution over CO2 Levels'
        new_chart = TwoAxesInstanciatedChart('CO2 Levels', 'Health', chart_name=chart_name)
        new_series = InstanciatedSeries(co2, health_data, 'Health', 'lines')
        new_chart.series.append(new_series)
        instanciated_charts.append(new_chart)

        return instanciated_charts

    def cost_evolution(cost_data, instanciated_charts):
    
        co2 = self.get_sosdisc_inputs('CO2_emissions')
    
        chart_name = 'Cost Evolution over CO2 Levels'
        new_chart = TwoAxesInstanciatedChart('CO2 Levels', 'Cost', chart_name=chart_name)
        new_series = InstanciatedSeries(co2, cost_data, 'Cost', 'lines')
        new_chart.series.append(new_series)
        instanciated_charts.append(new_chart)

        return instanciated_charts


    def get_post_processing_list(self, chart_filters=None):

            # For the outputs, making a graph for tco vs year for each range and for specific
            # value of ToT with a shift of five year between then

        instanciated_charts = []

        # Overload default value with chart filter
        if chart_filters is not None:
            for chart_filter in chart_filters:
                if chart_filter.filter_key == 'charts':
                    chart_list = chart_filter.selected_values
            
        if 'BioLoss' in chart_list:
            BioLoss_data= self.get_sosdisc_outputs('BioLoss')
            instanciated_charts = bioloss_evolution(BioLoss_data, instanciated_charts)

        if 'Cost' in chart_list:
            cost_data = self.get_sosdisc_outputs('Cost')
            instanciated_charts = cost_evolution(cost_data, instanciated_charts)

        if 'Health' in chart_list:
            health_data= self.get_sosdisc_outputs('Health')
            instanciated_charts = health_evolution(health_data, instanciated_charts)
            
        return instanciated_charts