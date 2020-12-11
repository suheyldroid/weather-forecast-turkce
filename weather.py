import requests
import pyttsx3
import time
parameters_for_api = {"apikey":"{your-api-key}","language":"en-us","details":"false","metric":"true"}
response = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/1day/222191",params=parameters_for_api)
response = response.json()

speaker = pyttsx3.init()

turkce_gunler = {"Mon":"Pazartesi","Tue":"Salı","Wed":"Çarşamba","Thu":"Perşembe","Fri":"Cuma","Sat":"Cumartesi","Sun":"Pazar"}
turkce_aylar = {"Jan":"Ocak", "Feb":"Şubat", "Mar":"Mart",
                "Apr":"Nisan", "May":"Mayıs", "Jun":"Haziran",
                "Jul":"Temmuz", "Aug":"Ağustos", "Sep":"Eylül",
                "Oct":"Ekim", "Nov":"Kasım", "Dec":"Aralık"}
gunluk_tabirler = {"Sunny":"Güneşli","Mostly sunny":"Genel olarak güneşli","Partly sunny":"Parçalı güneşli","Intermittent clouds":"Parçalı bulutlu",
                   "Hazy sunshine":"Puslu güneş","Mostly cloudy":"Genel olarak bulutlu","Cloudy":"Bulutlu","Dreary (Overcast)":"Kasvetli(Kapalı)",
                   "Fog":"Sisli","Showers":"Sağanak yağışlı","Mostly Cloudy w/ Showers":"Genel olarak bulutlu ve sağanak yağışlı",
                   "Partly Sunny w/ Showers":"Parçalı güneşli ve sağanak yağışlı","T-Storms":"Gökgürültülü fırtınalı","Mostly Cloudy w/ T-Storms":"Genel olarka bulutlu ve gök gürültülü",
                   "Partly Sunny w/ T-Storms":"Parçalı güneşli ve gökgürültülü fırtınalı","Rain":"Yağmurlu","Flurries":"Kısa ve şiddetli yağışlı","Mostly Cloudy w/ Flurries":"Genel olarka bulutlu ve kısa ve şiddetli yağışlı",
                   "Partly Sunny w/ Flurries":"Parçalı güneşli ve kısa ve şiddetli yağışlı","Snow":"Karlı","Mostly Cloudy w/ Snow":"Genel olarka bulutlu ve karlı","Ice":"Dolu yağışlı","Sleet":"Sulu kar",
                   "Freezing Rain":"Dondurucu yağmur","Rain and Snow":"Yağmur ve karlı","Hot":"Ateşli","Cold":"Soğuk","Windy":"Rüzgarlı","Clear":"Açık","Mostly clear":"Çok açık",
                   "Partly Cloudy":"Parçalı bulutlu","Hazy Moonlight":"Puslu ay"}

def maxTemp(apiResponse):
    max_temp = apiResponse["DailyForecasts"][0]["Temperature"]["Maximum"]
    return (max_temp["Value"], max_temp["Unit"])

def minTemp(apiResponse):
    min_temp = apiResponse["DailyForecasts"][0]["Temperature"]["Minimum"]
    return (min_temp["Value"], min_temp["Unit"])

def justASuggestion(apiResponse):
    return apiResponse["Headline"]["Text"]

def todayInTurkish():
    curr = time.ctime().split()
    curr[0], curr[1] = turkce_gunler[curr[0]], turkce_aylar[curr[1]]
    curr = [curr[2],curr[1],curr[4],curr[0]]
    return " ".join(curr)

def precipitation(apiResponse):
    night_prec = apiResponse["DailyForecasts"][0]["Night"]["HasPrecipitation"]
    day_prec = apiResponse["DailyForecasts"][0]["Day"]["HasPrecipitation"]
    if night_prec and day_prec:
        return "Bugün hem sabah hem akşam yağışlı"
    elif night_prec:
        return "Bugün sadece akşam yağışlı"
    elif day_prec:
        return "Bugün sadece sabah yağışlı"
    else:
        return "Bugün yağış görünmüyor"

def sumPhrase(apiResponse):
    day = gunluk_tabirler.get(apiResponse["DailyForecasts"][0]["Day"]["IconPhrase"],",bir şeyler ters gitti bir baksana,")
    night = gunluk_tabirler.get(apiResponse["DailyForecasts"][0]["Night"]["IconPhrase"],",bir şeyler ters gitti bir baksana,")
    return (day,night)

def forecastTeller(apiResponse):
    speaker.say("Bugün : {}.".format(todayInTurkish()))
    speaker.setProperty('voice', "com.apple.speech.synthesis.voice.Alex")
    speaker.say(justASuggestion(apiResponse))
    speaker.setProperty('voice', "com.apple.speech.synthesis.voice.yelda.premium")
    speaker.say("Bugün Hava: Minimum {} °{}, ve maksimum {} °{}. Dahası, sabah: {} ve akşam da: {}.".format(*minTemp(apiResponse),*maxTemp(apiResponse),*sumPhrase(apiResponse)))
    speaker.say(precipitation(apiResponse))
    speaker.runAndWait()
def forecastPrinter(apiResponse):
    print("Bugün : {}.".format(todayInTurkish()))
    print("Küçük bir tavsiye: {}".format(justASuggestion(apiResponse)))
    print("Bugün Hava: Minimum {} °{}, ve maksimum {} °{}. Dahası, sabah: {} ve akşam da: {}.".format(*minTemp(apiResponse),*maxTemp(apiResponse),*sumPhrase(apiResponse)))
    print(precipitation(apiResponse))

if __name__ == "__main__":
    forecastPrinter(response)
    forecastTeller(response)
    input("Lütfen çıkmak için enter'a basınız!")
    exit()
