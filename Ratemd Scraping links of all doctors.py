from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
# import sys
# sys.setdefaultencoding()

driver = webdriver.Chrome(r"D:\Tools\chromedriver_win32\chromedriver.exe")
browser = driver.get("https://www.ratemds.com/best-doctors/?country=us&specialty=dentist")
content = driver.page_source
soup = BeautifulSoup(content)

#last page details
page_list = soup.find_all("ul", class_="pagination pagination-sm")
last_page = 0
for page in page_list:
     li = page.find_all("li")
     last_page = int(li[-2].text)
# print(last_page)

Page_links = []
for p in range(1, last_page + 1):
     link = "https://www.ratemds.com/best-doctors/?specialty=dentist&page="+str(p)+"&country=us"
     Page_links.append(link)
#print(links)

Doctors_Links = []
Doctors_Name = []
for i in Page_links[0:2]:
    driver = webdriver.Chrome(r"D:\Tools\chromedriver_win32\chromedriver.exe")
    browser = driver.get(i)
    content = driver.page_source
    T_soup = BeautifulSoup(content)
    for name in T_soup.find_all('h2',attrs={'class':'search-item-doctor-name'}):
        Doctors_Name.append(name.text)
    for link in T_soup.find_all('a', attrs={'class': 'search-item-doctor-link'}):
        link = "https://www.ratemds.com/"+str(link.get('href'))
        # print(link)
        Doctors_Links.append(link)
    driver.close()

#Writing all the pages of doctors
data = {'Name':Doctors_Name,'Doctor link':Doctors_Links}
df = pd.DataFrame(data, columns= ['Name','Doctor link'])
df.to_csv (r'C:\Users\govar\Desktop\export_dataframe2.csv', index = False, header=True)
# print (df)

#Writing all the pages of dentist speciality
data = {'Dentist link':Page_links}
df = pd.DataFrame(data, columns= ['Dentist link'])
df.to_csv (r'C:\Users\govar\Desktop\export_dataframe1.csv', index = False, header=True)
# print (df)
Doctor_Name = []
review_list = []
was_this_useful = []
Staff_rating = []
Punctuality_rating = []
# Helpfulness_rating = []
# Knowledge_rating = []
# Date_rating =[]
# Star_rating = []
for i in Doctors_Links[0:2]:
    driver = webdriver.Chrome(r"D:\Tools\chromedriver_win32\chromedriver.exe")
    browser = driver.get(i)
    content = driver.page_source
    dr_soup = BeautifulSoup(content)
    No_of_Reviews = 0
    D_Name = dr_soup.find("h1", itemprop="name").text
    print(D_Name)
    Review_page_list = dr_soup.find_all("ul", class_="pagination pagination-sm")
    Review_last_page = 0
    for review_page in Review_page_list:
        lis = review_page.find_all("li")
        # print (lis)
        Review_last_page = int(lis[-2].text)
    print(Review_last_page)
    rp = 1
    # while rp <= 3:
    while rp <= Review_last_page:
        link = i + "?page=" + str(rp)
        driver = webdriver.Chrome(r"D:\Tools\chromedriver_win32\chromedriver.exe")
        browser = driver.get(link)
        content = driver.page_source
        review_soup = BeautifulSoup(content)
        print link
        r_text = review_soup.find_all("div", attrs={"itemprop": "review"})
        r_list = [r.find("div",attrs={"itemprop": "reviewBody"}).text for r in r_text]
        wtu = [r.find("span",class_="voteCount").text for r in r_text]
        s_rating = [r.find("div",attrs={"class": "rating-number Staff"}).text for r in r_text]
        p_rating = [r.find("div",attrs={"class": "rating-number Punctuality"}).text for r in r_text]
        H_rating = [r.find("div",attrs={"class": "rating-number Helpfulness"}).text for r in r_text]
        K_rating = [r.find("div",attrs={"class": "rating-number Knowledge"}).text for r in r_text]
        D_rating = [r.find("p",attrs={"class": "rating-comment-created pull-right"}).text for r in r_text]
        Star_full_rating = [r.find_all("span",attrs={"class": "star selected"}) for r in r_text]
        Star_half_rating = [r.find_all("span", attrs={"class": "star half"})for r in r_text]
        print(Star_full_rating)
        print(Star_half_rating)
        review_list += [d.encode('utf-8') for d in r_list]
        No_of_Reviews += len(r_list)
        print(No_of_Reviews)
        d = 0
        while d < len(r_list):
            Doctor_Name.append(D_Name)
            K = len(Star_full_rating[d]) + (len(Star_half_rating[d])*0.5)
            Star_rating.append(K)
            d += 1
        print(Doctor_Name)
        print Star_rating
        was_this_useful += wtu
        Staff_rating += [d.split(" ")[2] for d in s_rating]
        Punctuality_rating += [d.split(" ")[2] for d in p_rating]
        Helpfulness_rating += [d.split(" ")[2] for d in H_rating]
        Knowledge_rating += [d.split(" ")[2] for d in K_rating]
        Date_rating += D_rating
        rp += 1

        # print (review_list)
    # data = {'Doctor Name': Doctor_Name, 'Doctor Review': review_list, 'Was this Useful': was_this_useful,
    #         'Staff_rating': Staff_rating, 'Punctuality_rating': Punctuality_rating,
    #         'Helpfulness_rating': Helpfulness_rating, 'Knowledge_rating': Knowledge_rating,
    #         'Date of review': Date_rating}
    # df = pd.DataFrame(data,
    #                 columns=['Doctor Name', 'Doctor Review', 'Was this Useful', 'Staff_rating', 'Punctuality_rating',
    #                            'Helpfulness_rating', 'Knowledge_rating', 'Date of review'])
    # print(df)
        # if Doc_No == 1:
        #     df.to_csv(r'C:\Users\govar\Desktop\Review_list.csv', index=False, header=True)
        # else:
        #     df.to_csv(r'C:\Users\govar\Desktop\Review_list.csv', mode='a',index=False, header=False)
        # driver.close()
    # df.to_csv(r'C:\Users\govar\Desktop\Review_list.csv',mode='a',index=False, header=True)
    # print(df)
# data = {'Doctor Name':Doctors_Name}
# df = pd.DataFrame(data,columns=['Doctor Name'])
# df.to_csv(r'C:\Users\govar\Desktop\Review_list.csv', mode='a', index=False, header=True)
#     Doc_No += 1
    # driver.close()
data = {'Doctor Name':Doctor_Name,'Doctor Review':review_list,'Review Rating':Star_rating,'Was this Useful':was_this_useful,'Staff_rating':Staff_rating,'Punctuality_rating':Punctuality_rating,'Helpfulness_rating':Helpfulness_rating,'Knowledge_rating':Knowledge_rating,'Date of review':Date_rating}
df = pd.DataFrame(data, columns= ['Doctor Name','Doctor Review','Review Rating','Was this Useful','Staff_rating','Punctuality_rating','Helpfulness_rating','Knowledge_rating','Date of review'])
df.to_csv (r'C:\Users\govar\Desktop\Review_list.csv', index = False, header=True)
print (df)
# print (No_of_Reviews)
# print (review_list)
# print (was_this_useful)
# print (Staff_rating)
# print (Punctuality_rating)
# print (Helpfulness_rating)
# print (Knowledge_rating)
# print (Date_rating)