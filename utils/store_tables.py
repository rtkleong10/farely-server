from farely_api.boundary import DataGovService, LTADataMallService
import json

with open('data/fare_table.json', 'w') as file:
	data = DataGovService.getFareTable()
	json_data = {}

	for i in data:
		json_data[i] = {}

		for j in data[i]:
			json_data[i][str(j)] = data[i][j]

	json.dump(json_data, file)

with open('data/bus_services.json', 'w') as file:
	data = LTADataMallService.getBusServices()
	json.dump(data, file)