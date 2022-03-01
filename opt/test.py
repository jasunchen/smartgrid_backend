from optimization import *
from parse import *
from sklearn.metrics import r2_score

#initial time, base load, solar load, powerwall, grid usage, battery charge
def findRange(arr): 
    continuous = False
    ranges = []
    for index, i in enumerate(arr):
        if i == 1:
            if continuous == False:
                continuous = True 
                ranges.append([index, index+1])
        elif len(ranges) != 0 and continuous == True:
            continuous = False
            ranges[-1][-1] = index
    return ranges

def convertIndexToTime(index): #0-96, 0 being 00:00, 96 being 24:00
	if (index == 96):
		return "11:59 PM"

	hours = index // 4
	minutes = (index % 4)*15
	if minutes == 0:
		minutes = "00"

	time = "AM"
	if hours >= 12:
		hours -= 12
		time = "PM"

	if hours == 0:
		hours = 12

	return "{}:{} {}".format(hours, minutes, time)


def convertRangeToTimes(arr):
	length = len(arr)
	output = ""
	for index, ele in enumerate(arr):
		if (ele[0] == ele[1]):
			output += convertIndexToTime(ele[0])
		else:
			output += convertIndexToTime(ele[0]) + " to " + convertIndexToTime(ele[1])

		if (index == length - 2):
			output += ", and "
		else: 
			output += ", "

	return output[:-2]

def compareTimes():
    pass

#schedule ["", isOn, timeofday]
#inputs: baseload to test on, flexible load to schedule, schedule of flexible load, initial battery state, solar generation, number of dates
#outputs: utility usage, solar integration 
def checkTime(batterystate, batterySize, baseLoad, solar, shouldCharge, flexibleLoad, day, timeOfDay):
    entire_home_usage = sum(baseLoad) + sum(flexibleLoad)
    entire_solar_gen = sum(solar)

    if shouldCharge:
        for ind, ele in enumerate(flexibleLoad):
            baseLoad[day*96 + timeOfDay + ind] += ele

    energyFlow = computeEnergyFlow(solar, baseLoad)
    costGrid, costRenewableIntegration, excessSolar, excessBattery, utility, temp_battery= computePredictedBatteryChargeAndTotalCost(batterystate, energyFlow, 20, batterySize)
    solarToGrid = sum([item*1000 for item in utility if item >= 0])
    gridUsage = sum([item*-1000 for item in utility if item <= 0])

    return  (gridUsage/entire_home_usage, solarToGrid/entire_solar_gen, baseLoad, temp_battery[-1])





if __name__ == "__main__":
    #fileName = "data/battery.csv"
    fileNames = ["tesla2-14", "tesla2-15","tesla2-16","tesla2-17","tesla2-18","tesla2-19","tesla2-20"]
    dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    fileName = "data/feb7testingweek.xlsx"

    #feb14
    #pred_solar = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 48, 163, 285, 432, 510, 591, 666, 732, 793, 848, 897, 939, 979, 1014, 1039, 1064, 1089, 1104, 1113, 1121, 1123, 1114, 1095, 1071, 1043, 1013, 982, 943, 893, 843, 791, 727, 660, 585, 503, 418, 328, 236, 152, 80, 25, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 33, 167, 310, 435, 512, 591, 664, 730, 791, 848, 902, 948, 983, 1015, 1038, 1053, 1070, 1086, 1101, 1105, 1103, 1107, 1105, 1086, 1061, 1031, 990, 951, 908, 853, 790, 726, 657, 583, 507, 422, 332, 240, 154, 80, 25, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 177, 314, 426, 513, 591, 660, 728, 790, 838, 886, 933, 975, 1010, 1044, 1087, 1105, 1124, 1121, 1108, 1110, 1107, 1097, 1064, 1032, 1010, 977, 941, 896, 851, 788, 725, 656, 583, 503, 422, 335, 243, 158, 84, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 57, 185, 312, 442, 523, 602, 674, 738, 798, 852, 903, 951, 973, 1023, 1061, 1081, 1099, 1107, 1115, 1116, 1119, 1114, 1100, 1077, 1050, 1021, 987, 943, 898, 848, 789, 724, 656, 585, 508, 427, 341, 249, 169, 92, 34, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 49, 171, 303, 447, 521, 599, 671, 736, 794, 848, 898, 943, 984, 1018, 1044, 1073, 1098, 1115, 1122, 1119, 1115, 1106, 1089, 1071, 1052, 1026, 987, 944, 903, 856, 799, 736, 669, 596, 517, 433, 344, 253, 166, 91, 33, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 66, 204, 320, 434, 534, 592, 692, 720, 776, 865, 890, 907, 947, 984, 1057, 1044, 1114, 1149, 1141, 1136, 1090, 1030, 1038, 1049, 981, 934, 930, 980, 882, 818, 723, 645, 592, 532, 503, 472, 381, 252, 162, 117, 55, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 70, 195, 321, 436, 530, 621, 703, 774, 846, 930, 1023, 1014, 1063, 1100, 1129, 1152, 1108, 1112, 1136, 1142, 1138, 1128, 1107, 1080, 1055, 1021, 985, 944, 893, 836, 767, 741, 689, 273, 79, 58, 346, 194, 69, 76, 18, -15, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20]
    
    pred_solar = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 153, 299, 419, 509, 587, 661, 730, 795, 846, 894, 938, 980, 1022, 1051, 1077, 1089, 1101, 1116, 1125, 1119, 1119, 1109, 1080, 1049, 1023, 986, 944, 899, 845, 792, 731, 662, 584, 503, 417, 326, 231, 145, 72, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 45, 157, 283, 420, 507, 593, 671, 742, 799, 855, 871, 928, 958, 1013, 967, 1024, 1029, 1092, 1041, 1074, 1085, 1113, 1101, 1080, 1068, 1020, 1014, 864, 761, 759, 711, 734, 679, 576, 439, 414, 313, 219, 130, 46, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 48, 163, 285, 432, 510, 591, 666, 732, 793, 848, 897, 939, 979, 1014, 1039, 1064, 1089, 1104, 1113, 1121, 1123, 1114, 1095, 1071, 1043, 1013, 982, 943, 893, 843, 791, 727, 660, 585, 503, 418, 328, 236, 152, 80, 25, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 33, 167, 310, 435, 512, 591, 664, 730, 791, 848, 902, 948, 983, 1015, 1038, 1053, 1070, 1086, 1101, 1105, 1103, 1107, 1105, 1086, 1061, 1031, 990, 951, 908, 853, 790, 726, 657, 583, 507, 422, 332, 240, 154, 80, 25, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 177, 314, 426, 513, 591, 660, 728, 790, 838, 886, 933, 975, 1010, 1044, 1087, 1105, 1124, 1121, 1108, 1110, 1107, 1097, 1064, 1032, 1010, 977, 941, 896, 851, 788, 725, 656, 583, 503, 422, 335, 243, 158, 84, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 57, 185, 312, 442, 523, 602, 674, 738, 798, 852, 903, 951, 973, 1023, 1061, 1081, 1099, 1107, 1115, 1116, 1119, 1114, 1100, 1077, 1050, 1021, 987, 943, 898, 848, 789, 724, 656, 585, 508, 427, 341, 249, 169, 92, 34, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 49, 171, 303, 447, 521, 599, 671, 736, 794, 848, 898, 943, 984, 1018, 1044, 1073, 1098, 1115, 1122, 1119, 1115, 1106, 1089, 1071, 1052, 1026, 987, 944, 903, 856, 799, 736, 669, 596, 517, 433, 344, 253, 166, 91, 33, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 66, 204, 320, 434, 534, 592, 692, 720, 776, 865, 890, 907, 947, 984, 1057, 1044, 1114, 1149, 1141, 1136, 1090, 1030, 1038, 1049, 981, 934, 930, 980, 882, 818, 723, 645, 592, 532, 503, 472, 381, 252, 162, 117, 55, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    historical_baseload_avg = [202.81, 194.58, 201.93, 191.39, 182.69, 173.9, 152.74, 148.41, 156.21, 152.03, 145.35, 131.46, 145.11, 131.88, 113.24, 126.82, 123.58, 117.17, 105.16, 117.01, 124.4, 124.16, 136.53, 153.96, 195.83, 188.04, 206.4, 185.39, 157.31, 162.97, 167.69, 157.64, 154.85, 168.95, 180.86, 184.54, 188.6, 211.03, 239.68, 235.96, 240.09, 240.21, 255.46, 256.34, 271.9, 271.71, 284.37, 276.12, 274.44, 280.25, 273.16, 255.94, 259.27, 263.37, 258.82, 253.67, 237.28, 245.57, 238.39, 230.99, 213.81, 210.52, 219.89, 212.48, 199.15, 195.35, 218.14, 209.27, 190.1, 160.07, 153.15, 131.11, 114.27, 101.31, 101.25, 113.19, 118.95, 123.82, 125.34, 123.33, 125.79, 133.73, 128.9, 127.8, 129.78, 120.72, 125.98, 138.6, 139.75, 122.82, 124.05, 121.42, 195.17, 198.38, 219.35, 219.91]
    filtered_base = [291.67, 233.34, 291.67, 241.67, 266.67, 283.33, 150.0, 91.67, 125.0, 183.33, 108.33, 83.33, 108.34, 125.0, 141.67, 116.66, 108.34, 100.0, 133.33, 91.67, 108.34, 108.34, 108.33, 125.0, 108.33, 125.0, 108.33, 91.66, 175.0, 125.0, 125.0, 200.0, 408.33, 200.0, 258.33, 225.0, 275.0, 258.34, 266.67, 183.33, 216.67, 233.33, 225.0, 208.33, 275.0, 250.0, 208.34, 233.34, 266.67, 266.67, 216.66, 233.33, 233.33, 233.34, 216.66, 308.34, 225.0, 291.67, 233.33, 358.33, 216.67, 241.66, 191.67, 216.67, 175.0, 216.67, 200.0, 216.67, 225.0, 216.66, 166.66, 208.33, 233.34, 283.33, 266.66, 300.0, 258.34, 275.0, 258.33, 258.33, 275.0, 316.67, 300.0, 325.0, 316.67, 283.33, 333.34, 350.0, 218.1650561797752, 218.1650561797752, 218.1650561797752, 218.1650561797752, 218.16505617977518, 218.16505617977518, 218.16505617977518, 218.16505617977518, 218.16505617977515, 218.16505617977515, 218.16505617977515, 218.16505617977515, 218.16505617977515, 218.16505617977515, 218.16505617977515, 218.16505617977515, 218.16505617977515, 218.16505617977515, 218.16505617977512, 218.16505617977512, 218.16505617977512, 218.16505617977512, 218.16505617977512, 218.1650561797751, 218.1650561797751, 218.1650561797751, 218.1650561797751, 218.1650561797751, 218.1650561797751, 218.16505617977506, 218.16505617977506, 218.16505617977506, 218.16505617977506, 218.16505617977506, 218.16505617977506, 218.16505617977506, 218.16505617977504, 218.16505617977504, 218.16505617977504, 218.16505617977504, 241.67, 275.0, 283.33, 341.67, 416.67, 316.66, 266.67, 333.33, 283.34, 258.33, 358.34, 325.0, 350.0, 308.33, 291.67, 266.66, 316.67, 275.0, 291.67, 283.33, 283.33, 250.0, 333.33, 283.34, 241.67, 241.66, 266.66, 250.0, 225.0, 250.0, 258.33, 200.0, 225.0, 300.0, 200.0, 241.66, 275.0, 208.33, 216.67, 191.66, 250.0, 241.67, 241.66, 241.67, 250.0, 200.0, 216.66, 250.0, 325.0, 275.0, 250.0, 300.0, 291.67, 208.34, 208.33, 300.0, 300.0, 325.0, 325.0, 341.67, 291.67, 275.0, 216.66, 283.33, 241.67, 233.33, 200.0, 425.0, 208.33, 175.0, 158.33, 158.33, 108.33, 116.67, 125.0, 116.66, 108.34, 108.33, 91.66, 133.33, 108.33, 125.0, 125.0, 183.34, 116.66, 100.0, 91.67, 141.67, 83.33, 108.34, 83.33, 125.0, 150.0, 158.33, 175.0, 425.0, 200.0, 191.66, 225.0, 216.67, 250.0, 316.67, 225.0, 258.33, 358.33, 233.33, 275.0, 258.33, 300.0, 308.33, 291.66, 241.67, 275.0, 275.0, 283.33, 325.0, 241.67, 241.67, 325.0, 216.67, 241.66, 316.67, 225.0, 233.33, 241.67, 225.0, 183.33, 191.67, 150.0, 200.0, 175.0, 150.0, 225.0, 808.33, 158.33, 191.67, 525.0, 933.34, 491.67, 216.66, 258.34, 258.33, 208.34, 383.34, 416.66, 300.0, 266.67, 250.0, 225.0, 241.67, 316.67, 250.0, 233.33, 283.33, 225.0, 200.0, 200.0, 158.33, 133.33, 183.33, 141.67, 266.67, 408.33, 133.33, 225.0, 125.0, 100.0, 150.0, 141.67, 75.0, 158.34, 233.34, 208.33, 191.67, 175.0, 191.66, 166.67, 150.0, 166.66, 150.0, 91.66, 108.34, 133.33, 133.33, 116.67, 158.34, 233.33, 225.0, 166.67, 158.33, 283.33, 233.33, 266.67, 300.0, 366.67, 275.0, 291.67, 391.67, 283.33, 325.0, 300.0, 308.34, 300.0, 291.67, 325.0, 291.67, 291.67, 283.33, 316.67, 291.66, 291.66, 425.0, 308.33, 333.33, 400.0, 491.66, 308.34, 441.67, 383.34, 291.67, 258.33, 250.0, 308.33, 233.33, 266.66, 350.0, 241.67, 233.33, 275.0, 166.66, 166.67, 183.33, 191.67, 741.67, 883.33, 783.34, 408.33, 266.67, 233.33, 266.67, 266.67, 275.0, 233.33, 233.33, 250.0, 275.0, 200.0, 208.33, 350.0, 341.67, 691.67, 333.33, 341.67, 258.34, 275.0, 191.67, 258.33, 250.0, 241.67, 241.67, 275.0, 241.67, 150.0, 175.0, 116.66, 108.34, 216.67, 91.67, 83.33, 141.67, 150.0, 108.33, 116.67, 100.0, 150.0, 125.0, 83.33, 108.34, 166.66, 91.67, 83.33, 191.66, 233.34, 166.67, 183.34, 200.0, 225.0, 408.34, 208.33, 283.33, 316.67, 308.33, 291.67, 375.0, 400.0, 308.34, 350.0, 525.0, 583.34, 525.0, 400.0, 375.0, 400.0, 508.3299999999999, 366.66, 308.34, 433.33, 433.33, 350.0, 333.34, 266.67, 483.33, 300.0, 200.0, 241.67, 366.66, 908.33, 675.0, 641.67, 425.0, 425.0, 591.67, 775.0, 516.67, 400.0, 441.67, 241.66, 200.0, 333.34, 875.0, 1191.66, 950.0, 350.0, 333.33, 366.67, 333.33, 483.33, 525.0, 633.33, 800.0, 600.0, 558.33, 766.67, 775.0, 625.0, 583.33, 408.34, 333.33, 266.66, 216.67, 300.0, 383.34, 266.66, 350.0, 600.0, 250.0, 300.0, 325.0, 233.33, 150.0, 158.33, 158.34, 200.0, 191.67, 208.33, 241.66, 166.67, 158.33, 150.0, 216.67, 133.33, 83.33, 116.67, 150.0, 350.0, 241.67, 308.34, 150.0, 125.0, 108.33, 125.0, 158.34, 175.0, 183.34, 200.0, 158.33, 191.67, 258.33, 183.33, 400.0, 233.33, 258.33, 275.0, 208.34, 275.0, 250.0, 208.33, 291.67, 258.33, 233.33, 250.0, 300.0, 291.66, 250.0, 225.0, 283.34, 225.0, 216.67, 283.34, 208.34, 233.33, 250.0, 216.67, 191.67, 183.33, 183.33, 191.66, 150.0, 183.34, 266.66, 166.67, 166.66, 191.66, 200.0, 208.33, 241.66, 216.67, 225.0, 166.67, 175.0, 266.67, 191.66, 175.0, 216.67, 208.34, 175.0, 208.34, 166.67, 216.67, 241.67, 175.0, 166.66, 191.66, 133.34, 125.0, 183.33, 116.67, 133.33, 175.0, 141.67, 116.67, 150.0, 116.67, 150.0, 133.34, 125.0, 133.34, 158.34, 125.0, 125.0, 150.0, 108.33, 100.0, 125.0, 141.67, 116.67, 108.34, 141.67, 150.0, 125.0, 100.0, 116.67, 158.33, 108.33, 83.33, 125.0, 166.66, 133.33, 125.0, 175.0, 200.0, 316.67, 200.0, 258.33, 191.67, 208.33, 250.0, 250.0, 233.34, 250.0, 233.33, 266.67, 241.67, 225.0, 283.33, 266.67, 258.34, 275.0, 250.0, 241.67, 216.67, 258.34, 241.67, 183.34, 225.0, 283.34, 166.67, 175.0, 233.33, 175.0, 158.33, 166.66, 175.0, 166.67, 191.67, 183.33, 216.66, 166.66, 141.67, 200.0, 191.66, 183.34, 175.0, 216.67, 216.67, 191.66, 183.34, 200.0, 191.67, 200.0, 216.66, 175.0, 191.67, 233.33, 208.34, 175.0, 275.0, 275.0, 283.34, 266.67, 233.33, 308.33, 325.0, 216.66]
    filtered_base = filtered_base + historical_baseload_avg
    filtered_flex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1048.494943820225, 1073.504943820225, 1106.8349438202247, 1081.834943820225, 1040.1649438202248, 1131.834943820225, 1090.1749438202246, 990.1649438202247, 1240.1649438202246, 1148.5049438202248, 1265.1749438202246, 940.1649438202246, 948.5049438202249, 940.1749438202248, 831.8349438202249, 848.4949438202251, 798.4949438202248, 781.8349438202249, 856.8349438202248, 948.504943820225, 865.1649438202248, 865.1649438202248, 890.164943820225, 856.8349438202248, 840.1649438202248, 881.834943820225, 881.834943820225, 831.8349438202249, 823.4949438202249, 798.504943820225, 765.1649438202251, 865.164943820225, 840.164943820225, 806.8349438202249, 956.834943820225, 1006.8349438202251, 865.164943820225, 1006.8349438202251, 948.5049438202251, 356.83494382022496, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    filtered_flex_nozeroes = [i for i in filtered_flex if i != 0]

    #baseForecast = baseForecast*8

    #settings 
    weight1 = 1 #importance of cost 
    weight2 = 0 #importance of renewable integ
    weight3 = 0.5 #importance of shutoff
    lowerLimit = 20
    maximumLimit = 100
    shutOffRisk = 0
    idealReserveThreshold = 80
    

    #4 powerwalls = 4*13.5kwH = 54kWh 
    batterySize = 54000
    currentBatteryState1, currentBatteryState2, originalBatteryState = 0.802*batterySize, 0.802*batterySize, 0.802*batterySize

    pred_battery_tesla = []
    pred_battery_watthours = []
    entire_home = []
    entire_solar = []
    weekly_best_times = []
    actual_grid = []
    modeled_grid = []

    battery_level_from_forecasted = []
    gridUsage = 0
    solarToGrid = 0

    data = parseExcel(fileName)

    for ind, name in enumerate(dayNames):
        #print(currentBatteryState)

        time = [x[0] for x in data[ind]]
        home = [x[1] for x in data[ind]]
        solar = [x[2] for x in data[ind]]
        powerwall = [x[3] for x in data[ind]]
        grid = [x[4] for x in data[ind]]

        #extracting data
        actual_grid = actual_grid + grid
        entire_home = entire_home + home
        entire_solar = entire_solar + solar
        energyFlow = computeEnergyFlow(solar, home)
        costGrid, costRenewableIntegration, excessSolar, excessBattery, utility, temp_battery= computePredictedBatteryChargeAndTotalCost(currentBatteryState1, energyFlow, 20, batterySize)
        utility = utility[:96]
        solarToGrid += sum([item*1000 for item in utility if item >= 0])
        gridUsage += sum([item*-1000 for item in utility if item <= 0])
        modeled_grid = modeled_grid + utility[:96]
        # print(excessSolar)
        currentBatteryState1 = temp_battery[95]*1000
        pred_battery_watthours = pred_battery_watthours + temp_battery[:96]
        temp_battery = [round(item / (batterySize/1000), 2)*100 for item in temp_battery] #convert to battery percentage
        temp_battery = temp_battery[:96]
        pred_battery_tesla = pred_battery_tesla + temp_battery
    print("Original grid usage: {}%, solar to grid: {}%".format(gridUsage / sum(entire_home), solarToGrid/(sum(entire_solar))))

    val1, val2, u_, endingBatt = checkTime(originalBatteryState, batterySize, filtered_base[:672], entire_solar, True, filtered_flex_nozeroes, 0, 88)

    # val1, val2, u_ = checkTime(originalBatteryState, batterySize, filtered_base[:672], entire_solar, False, filtered_flex_nozeroes, 0, 88)
    print("With flex load grid usage: {}%, solar to grid: {}%".format(val1, val2))

    avgImprovedGridUsage, avgImprovedRenewableIntegration = 0,0

    for ind, name in enumerate(dayNames):
        #print(currentBatteryState)

        time = [x[0] for x in data[ind]]
        home = [x[1] for x in data[ind]]
        solar = [x[2] for x in data[ind]]
        powerwall = [x[3] for x in data[ind]]
        grid = [x[4] for x in data[ind]]


        # algorithm testing 
        #user_model = UserProfile(weight1, weight2, weight3, lowerLimit, maximumLimit, shutOffRisk, idealReserveThreshold, solarForecast, baseForecast, currentBatteryState, batterySize)
        #baseForecast = filtered_base[ind*96:ind*96+192]
        baseForecast = historical_baseload_avg*2
        solarForecast = pred_solar[ind*96:ind*96+192]

        user_model = UserProfile(weight1, weight2, weight3, lowerLimit, maximumLimit, shutOffRisk, idealReserveThreshold, solarForecast, baseForecast, currentBatteryState2, batterySize)

        # avg duration: 10.630434782608695 --> 11
        # avg charge: 10.854913043478252 --> 10854.91
        TeslaEV = FlexibleLoad("Tesla EV", 45791, 40) #example

        best_threshold, best_score, best_solar, best_battery, utility, battery = find_optimal_threshold(user_model)
        currentBatteryState2 = battery[95]*1000

        good_times, costCharge = find_good_times(user_model, best_threshold, TeslaEV)
        battery_level_from_forecasted = battery_level_from_forecasted + battery[:96]
        besttimes = convertRangeToTimes(findRange(good_times + [0]))
        weekly_best_times = weekly_best_times + good_times
        shouldCharge = should_charge(user_model, best_threshold, costCharge)
        print("Results for {}: Best threshold - {}, Should charge - {}, Best times - {}. ".format(name, best_threshold, shouldCharge, besttimes))

        val1, val2, u_, endingBatt = checkTime(originalBatteryState, batterySize, filtered_base[:672], entire_solar, shouldCharge, filtered_flex_nozeroes, ind, findRange(good_times + [0])[0][0])
        # print(u_)
        avgImprovedGridUsage += val1
        avgImprovedRenewableIntegration += val2
        print("Estimated performance if charging today at {}: {}%, solar to grid: {}%, with ending battery {}".format(convertIndexToTime(findRange(good_times + [0])[0][0]), val1, val2, round(endingBatt / (batterySize/1000), 2)*100 ))

        print("--------------------------------------------------------------------------")

    #model
    print("DATA:")
    # print(pred_battery_tesla)
    # print(entire_home)
    # print(actual_grid)
    # print(modeled_grid)

    #testing results
    print("RESULTS:")
    print("Avg improved gridusage: {}, Avg improved renewable integration: {}".format(avgImprovedGridUsage/7, avgImprovedRenewableIntegration/7))
    # battery_level_from_forecasted = [round(item / (batterySize/1000), 2)*100 for item in battery_level_from_forecasted] #convert to battery percentage
    # print(battery_level_from_forecasted)
    print(weekly_best_times)



    (home, solar, powerwall, grid, battery_level) = parse("data/feb7batt.csv")
    print(battery_level)
    #seeing improved performance
    #filtered_flex = 






    #diff = [real - pred for real, pred in zip(battery_level, pred_battery)]
    #r2 = r2_score(battery_level, pred_battery )
    #print(r2) #0.9759982805785794



    


