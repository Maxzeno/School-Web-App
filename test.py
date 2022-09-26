# import requests
# from bs4 import BeautifulSoup as soup
# import os
# # import cssutils

# class PageScaper:
#     def __init__(self, url=None, login_url='https://cdssenugu.org/portal/login/validate_login', domain_url=None):
#         self.url = url
#         self.login_url = login_url
#         self.domain_url = domain_url or '/'.join(url.split('/')[:3])


#     def get_static_urls(self):
#         with requests.session() as request:
#             self.session_login(request)
#             resp = request.get(self.url).text
#             parse = soup(resp, 'lxml')

#             links = parse.find_all('link')
#             imgs = parse.find_all('img')
#             scripts = parse.find_all('script')
#             # as_ = parse.find_all('a')

#             urls = [self.base_urler(link.attrs.get('href')) for link in links if self.base_urler(link.attrs.get('href'))]
#             urls += [self.base_urler(script.attrs.get('src')) for script in scripts if self.base_urler(script.attrs.get('src'))]
#             urls += [self.base_urler(img.attrs.get('src')) for img in imgs if self.base_urler(img.attrs.get('src'))]
#             # urls += [self.base_urler(a_.attrs.get('href')) for a_ in as_ if self.base_urler(a_.attrs.get('href'))]

#         return set(urls)


#     def get_page_urls(self, url=None):
#         the_url = url if url else self.url
#         with requests.session() as request:
#             self.session_login(request)
#             resp = request.get(the_url).text
#             parse = soup(resp, 'lxml')

#             as_ = parse.find_all('a')
#             forms = parse.find_all('form')

#             urls = [self.base_urler(a_.attrs.get('href')) for a_ in as_ if self.base_urler(a_.attrs.get('href'))]
#             ## do not send any request to those wheather GET, POST etc it DELETES things urls = [self.base_urler(a_.attrs.get('onclick').split("('")[1].split("',")[0]) for a_ in as_ if self.base_urler(a_.attrs.get('onclick'))]
#             urls += [self.base_urler(form.attrs.get('action')) for form in forms if self.base_urler(form.attrs.get('action'))]
#             print(set(urls))
#         return set(urls)


#     def base_urler(self, url):
#         if url:
#             if url.startswith(self.domain_url):
#                 return url
#             elif url.startswith('http://') or url.startswith('https://'):
#                 return None
#             else:
#                 if url.startswith('/'):
#                     return self.domain_url + url
#                 else:
#                     return self.domain_url + "/" + url
#         return  None


#     def download_static(self, urls_list=None, folder=''):
#         folder += '/' if folder else ''
#         if urls_list:
#             self.session_login(request)
#             urls = urls_list  
#         else:
#             urls = self.get_static_urls()

#         with requests.session() as request:
#             for url in urls:
#                 path = folder + '/'.join(url.split('/')[3:-1])
#                 try:
#                     os.makedirs(path)
#                 except FileExistsError:
#                     pass
                    
#                 file_name = path+"/"+url.split('/')[-1]
#                 print(file_name)
#                 if not os.path.exists(file_name):
#                     print('downloading ... ', file_name)
#                     file = open(file_name, 'wb')
#                     got = request.get(url)
#                     file.write(got.content)
#                     file.close()

#         return 'Done'

#     def download_page(self, url=None, page_type='html', folder='', folder_in=''):
#         folder += '/' + folder_in if folder_in else folder_in
#         the_url = url if url else self.url
#         with requests.session() as request:
#             self.session_login(request)
#             path = folder
#             try:
#                 os.makedirs(path)
#             except FileExistsError:
#                 pass

#             d_appender = ''
#             for i in range(1, len(the_url.split('/'))+1):
#                 if not the_url.split('/')[i*-1].isdigit():
#                     name = the_url.split('/')[i*-1] + d_appender
#                     break
#                 else:
#                     d_appender = '_' + the_url.split('/')[i*-1] if not d_appender else '_' + the_url.split('/')[i*-1] + d_appender
#             else:
#                 name = d_appender[1:]

#             file_name = path+"/"+name+'.' + page_type
#             if not os.path.exists(file_name):
#                 file = open(file_name, 'wb')
#                 got = request.get(the_url)
#                 file.write(got.content)
#                 file.close()
#                 return 'Done'
#             return f'File with same name Exists in \'{file_name} \''


#     def session_login(self, session):
#         # got = session.get(url).content
#         # parse = soup(got, 'lxml')
#         # csrf_token = parse.find_all('input', attrs={'id':'csrf_token'})[0].attrs.get('value')

#         posted = session.post(self.login_url, 
#             data={'email':'Commandant@cdssenugu.org', 'password':'VPAdmin'})

#         html = posted.content
#         status = posted.status_code
#         return session, html, status

# urls = {'https://cdssenugu.org/portal/admin/management_team', 
# 'https://cdssenugu.org/portal/login/logout', 
# 'https://cdssenugu.org/portal/admin/noticeboard', 
# 'https://cdssenugu.org/portal/admin/accountant', 
# 'https://cdssenugu.org/portal/admin/librarian', 
# 'https://cdssenugu.org/portal/admin/dashboard', 
# 'https://cdssenugu.org/portal/admin/event_calendar', 
# 'https://cdssenugu.org/portal/', 
# 'https://cdssenugu.org/portal/admin/principal_comment_codes', 
# 'https://cdssenugu.org/portal/admin/manage_class', 
# 'https://cdssenugu.org/portal/admin/pass_mark', 
# 'https://cdssenugu.org/portal/admin/profile', 
# 'https://cdssenugu.org/portal/admin/tabulation_sheet', 
# 'https://cdssenugu.org/portal/admin/invoice', 
# 'https://cdssenugu.org/portal/admin/cognitive_key_domain_scores', 
# 'https://cdssenugu.org/portal/admin/permission', 
# 'https://cdssenugu.org/portal/admin/promotion', 
# 'https://cdssenugu.org/portal/admin/expense_category', 
# 'https://cdssenugu.org/portal/admin/book', 
# 'https://cdssenugu.org/portal/admin/sb_description_score_manage', 
# 'https://cdssenugu.org/portal/admin/housemaster_comment_codes', 
# 'https://cdssenugu.org/portal/admin/student', 
# 'https://cdssenugu.org/portal/admin/class_room', 
# 'https://cdssenugu.org/portal/admin/teacher', 
# 'https://cdssenugu.org/portal/admin/expense', 
# 'https://cdssenugu.org/portal/admin/attendance', 
# 'https://cdssenugu.org/portal/admin/teacher_comment_codes', 
# 'https://cdssenugu.org/portal/admin/principal_subject_codes', 
# 'https://cdssenugu.org/portal/admin/book_issue', 
# 'https://cdssenugu.org/portal/admin/student/create', 
# 'https://cdssenugu.org/portal/admin/routine', 
# 'https://cdssenugu.org/portal/admin/mark', 
# 'https://cdssenugu.org/portal/admin/grade', 
# 'https://cdssenugu.org/portal/admin/subject', 
# 'https://cdssenugu.org/portal/admin/subject_permission', 
# 'https://cdssenugu.org/portal/admin/exam', 
# 'https://cdssenugu.org/portal/admin/syllabus', 
# 'https://cdssenugu.org/portal/admin/school_settings', 
# 'https://cdssenugu.org/portal/admin/parent', 
# 'https://cdssenugu.org/portal/admin/sb_description', 
# 'https://cdssenugu.org/portal/admin/department'}

# page_scraper = PageScaper('https://cdssenugu.org/portal/admin/department')

# # print(page_scraper.download_static(folder='static_store/dashboard'))
# # print(page_scraper.download_page(folder='static_store', folder_in='new'))
# # print(page_scraper.get_static_urls())



# lst_of_set = [page_scraper.get_page_urls(url) for url in  urls]
# print(lst_of_set)

# def unique_except_set(lst_of_set, except_url_list):
#     new_set = set()
#     def unique_x_url(set_iter, except_url_list):
#         return set_iter.difference(except_url_list)
#     for set_ in  lst_of_set:
#         new_set.update(set_)

#     return unique_x_url(new_set, except_url_list)

# for i in unique_except_set(lst_of_set, urls):
#     page_scraper.download_page(i, folder='static_store', folder_in='new')

# # resp = requests.get('http://127.0.0.1:8000/portal/admin/teacher').text
# # parse = soup(resp, 'lxml')

# # ds = parse.find_all('a')
# # urls = [d.attrs.get('onclick') for d in ds if d.attrs.get('onclick')]
# # for url in urls[:2]:
# #     print(url.split("('")[1].split("',")[0])
# #     page_scraper.download_page(url.split("('")[1].split("',")[0], folder='static_store', folder_in='new1')
# #     