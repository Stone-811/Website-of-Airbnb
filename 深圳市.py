# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time, json, csv
OpenFile = open("深圳市.csv", "w", newline = '', encoding = 'utf-8-sig')
OpenWriter = csv.writer(OpenFile)
#CityLists = ['北京', '上海', '深圳', '香港']
FrontPage = [0,18,36,54,72,90,108,126,144,162,180,198,216,234,252,270,288]
for i in FrontPage:
    #房屋ID爬取 - 放在explore_tabs
    FrontPageUrl = 'https://www.airbnb.cn/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&auto_ib=false&client_session_id=8ecfe97e-4d62-40c6-b51c-66d88a940983&currency=CNY&experiences_per_grid=20&federated_search_session_id=fe3f5059-4e4a-4c95-9d22-46e56ae75e33&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_offset='+ str(i) +'&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&last_search_session_id=b63b27d2-7fab-4004-b0fd-a166d23336c3&locale=zh&luxury_pre_launch=true&metadata_only=false&query=深圳&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=BjECAOJP&satori_version=1.1.3&screen_size=small&section_offset=7&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&version=1.4.5'
    FrontPageRes = requests.get(FrontPageUrl)
    AirbnbIDLists = []
    for j in json.loads(FrontPageRes.text)['explore_tabs'][0]['home_tab_metadata']['remarketing_ids']:
        AirbnbUrl = 'https://www.airbnb.cn/rooms/' + str(j) + '?s=Y9Ax4dqF&guests=1&adults=1'    
        #print(AirbnbUrl)
        PriceJsonUrl = 'https://www.airbnb.cn/api/v2/pdp_listing_booking_details?_format=for_web_dateless&_intents=p3_book_it&_interaction_type=pageload&_p3_impression_id=p3_1552968144_5SvVUuEDAHQIgc2j&_parent_request_uuid=565da801-7a75-49c0-8a1e-5aa27c04d2bc&currency=CNY&force_boost_unc_priority_message_type=&guests=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id='+ str(j) +'&locale=zh&number_of_adults=1&number_of_children=0&number_of_infants=0&show_smart_promotion=0'
        JsonUrl = 'https://www.airbnb.cn/api/v2/pdp_listing_details/'+ str(j) +'?_format=for_rooms_show&adults=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&'
        #limit是一次給多少留言數量，Offset是起始留言第幾封。
#####   #MesJsonUrl = 'https://www.airbnb.cn/api/v2/reviews?currency=CNY&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh&listing_id=' + str(j) + '&role=guest&_format=for_p3&_limit=100&_offset=0&_order=language_country'
        #AirbnbUrl = 'https://www.airbnb.cn/rooms/31027114?guests=1&adults=1'
        browser = webdriver.Firefox()
        AirbnbResult = browser.get(AirbnbUrl)
        time.sleep(5)#停滯時間10秒鐘，等待網頁合成。
        #print(browser.page_source)
        ####################################################################################################
        #用PriceJsonUrl爬取
        try:
            PriceJsonRes = requests.get(PriceJsonUrl)
            Price = json.loads(PriceJsonRes.text)['pdp_listing_booking_details'][0]['p3_display_rate']['amount']
            #用JsonUrl爬取
            JsonRes = requests.get(JsonUrl)
            #HouseID = json.loads(JsonRes.text)['pdp_listing_detail']['id']
            HouseType = json.loads(JsonRes.text)['pdp_listing_detail']['localized_room_type']
            localized_city = ''
            localized_city = json.loads(JsonRes.text)['pdp_listing_detail']['location_title']
            Bathroom = json.loads(JsonRes.text)['pdp_listing_detail']['bathroom_label'] #['accessibility_module']['amenities']
            Bed = json.loads(JsonRes.text)['pdp_listing_detail']['bed_label'] 
            Bedroom = json.loads(JsonRes.text)['pdp_listing_detail']['bedroom_label']
            Guest = json.loads(JsonRes.text)['pdp_listing_detail']['guest_label']
            MessageNum = json.loads(JsonRes.text)['pdp_listing_detail']['review_details_interface']['review_count']#['preview_tags']
            Host_intro_1 = json.loads(JsonRes.text)['pdp_listing_detail']['primary_host']['host_intro_tags'][0]#留言數
            Host_intro_2 = json.loads(JsonRes.text)['pdp_listing_detail']['primary_host']['host_intro_tags'][1]
            Host_intro = Host_intro_1 + '，' + Host_intro_2
            OtherFeature = json.loads(JsonRes.text)['pdp_listing_detail']['categorized_preview_amenities'][0]['amenities']
            ####################################################################################################
            #用MesJsonUrl爬取
            #MaxMes = (float(Host_intro_1)/100.0) + 1
            #MessageComments = []#留言內容
            #MessageTime = []#留言時間
            MessageTotal = []
            for i in range(int(MessageNum/100)+1):
                MesJsonUrl = 'https://www.airbnb.cn/api/v2/reviews?currency=CNY&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh&listing_id=%s&role=guest&_format=for_p3&_limit=100&_offset=%s&_order=language_country'%(str(j), i*100)
                MesJsonRes = requests.get(MesJsonUrl)
                for count in json.loads(MesJsonRes.text)['reviews']:
                    MessageAll = str(count['id']) + ';' + str(count['localized_date']) + ';' + str(count['comments'])
                    MessageTotal.append(MessageAll)
                    #MessageComments.append(count['comments'])
                    #MessageTime.append(count['localized_date'])
                    #print(count)
                ###Mes = json.loads(MesJsonRes.text)['reviews']['comments']
                ###MesTime = json.loads(MesJsonRes.text)['reviews']['localized_date']
                #用selenium爬取
            AirbnbSoup = BeautifulSoup(browser.page_source, 'html5lib')
            AccuracyScore = ' '
            CommunicationScore = ' '
            CleanScore = ' '
            LocationScore = ' '
            CheckinScore = ' '
            PriceScore = ' '
            Score = AirbnbSoup.find_all('div', class_='_1iu38l3')
            AccuracyScore = Score[0].find('span')['aria-label']#準確
            CommunicationScore = Score[1].find('span')['aria-label']#溝通
            CleanScore = Score[2].find('span')['aria-label']#乾淨
            LocationScore = Score[3].find('span')['aria-label']#位置
            CheckinScore = Score[4].find('span')['aria-label']#入住
            PriceScore = Score[5].find('span')['aria-label']#性價比
            print('房屋ID: %s' %(str(j)))
            print('房屋類型: %s' %(HouseType))
            print('區域: %s' %(localized_city))
            print('住房人數: %s'%(Guest))
            print('廁所: %s' %(Bathroom))
            print('床位: %s' %(Bed))
            print('臥室: %s' %(Bedroom))
            print('留言總數: %s' %(MessageNum))
            print('價格: %s' %(Price))
            print('房東獲得總留言數量: %s' %(Host_intro))
            print('準確性度分數: %s\n溝通性度分數: %s\n整潔性度分數: %s\n位置性度分數: %s\n入住性度分數: %s\n性價比性度分數: %s\n'%(AccuracyScore, CommunicationScore, CleanScore, LocationScore, CheckinScore, PriceScore))
            print('留言資訊: %s' %(MessageTotal))
            print('其他資訊: %s' %(OtherFeature))
            Data = [str(j), HouseType ,localized_city, Guest, Bathroom, Bed, Bedroom, MessageNum, Price, Host_intro, AccuracyScore, CommunicationScore, CleanScore, LocationScore, CheckinScore, PriceScore, MessageTotal, OtherFeature]
            OpenWriter.writerow(Data)
            browser.quit()        
        except:
            OpenWriter.writerow(AirbnbUrl + 'is Wrong')
            print(AirbnbUrl + 'is Wrong')
            browser.quit()
            
    #print('留言內容: %s' %(MessageComments))
    #print('留言時間: %s' %(MessageTime))

'''
searchBox = browser.find_element_by_class_name("_1cxn5bx2")
searchBox.send_keys('北京' + Keys.RETURN)

print(browser.page_source)
FileTxt = open("測試Airbnb網頁.txt", "w",encoding  = "cp1252")
FileTxt.write(browser.page_source)
FileTxt.close()
'''
#OpenWriter.close()
OpenFile.close()