from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from scraper.Domain import Profile
from scraper.Domain import License, Experience, Education
from scraper.models import UserProfileHtml
from django.contrib.auth.models import User
import time
import re


class Linkedin:
    @staticmethod
    def scroll(driver):
        start = time.time()

        initialScroll = 0
        finalScroll = 1000

        while True:
            driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
            finalScroll += 1000
            time.sleep(1)
            end = time.time()
            if round(end - start) > 20:
                break

    @staticmethod
    def login_with_cookie(driver, cookie):
        driver.get("https://www.linkedin.com/login")
        driver.add_cookie({
            "name": "li_at",
            "value": cookie
        })

    @staticmethod
    def get_general_info(html: str) -> Profile:
        soup = BeautifulSoup(html, 'lxml')
        name = soup.find(
            'h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip()
        try:
            title = soup.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
        except:
            title = ''

        try:
            description = soup.find('div', {
                'class': 'pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center'}).find('span').get_text().strip()
        except:
            description = ''

        try:
            location = soup.find(
                'span', {'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()
        except:
            location = ''
        return Profile(name=name, title=title, description=description, location=location)

    @staticmethod
    def get_contact_info(html: str, profile: Profile):
        soup = BeautifulSoup(html, 'lxml')
        email_r = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        try:
            profile.phone_number = soup.find(
                'li', {'class': 'pv-contact-info__ci-container t-14'}).find('span').get_text().strip()
        except:
            profile.phone_number = ''
        try:
            datas = soup.find_all(
                'div', {'class': 'pv-contact-info__ci-container t-14'})
            profile.email = ''
            for i in datas:
                current = i.find('a').get_text().strip()
                if (re.fullmatch(email_r, current)):
                    profile.email = current
                    break
        except:
            profile.email = ''
        try:
            profile.web_page = soup.find(
                'li', {'class': 'pv-contact-info__ci-container link t-14'}).find('a').get_text().strip()
        except:
            profile.web_page = ''

        return profile

    @staticmethod
    def get_certifications(html: str, profile: Profile) -> Profile:
        soup = BeautifulSoup(html, 'lxml')
        try:
            list_off_licenses = soup.find(
                'ul',
                {'class': 'pvs-list'}
            ).find_all('li', {'class', 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
        except:
            profile.licences = []

        for i in list_off_licenses:
            try:
                name = i.find(
                    'div',
                    {'class': 'display-flex align-items-center mr1 hoverable-link-text t-bold'}
                ).find('span').get_text().strip()

                try:
                    emitted_by = i.find('span', {'class': 't-14 t-normal'}).find('span').get_text().strip()
                except:
                    emitted_by = ''

                try:
                    expedition = i.find('span', {'class': 't-14 t-normal t-black--light'}
                                        ).find('span').get_text().strip().split(':')[-1].strip()
                except:
                    expedition = ''

                c_license = License(
                    name=name,
                    emitted_by=emitted_by,
                    expedition=expedition
                )
                profile.licences.append(c_license)
            except:
                continue

        return profile

    @staticmethod
    def get_experience(html: str, profile: Profile) -> Profile:
        soup = BeautifulSoup(html, 'lxml')

        try:
            list_off_experiences = soup.find(
                'ul',
                {'class': 'pvs-list'}
            ).find_all('li', {'class', 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
        except:
            profile.experiences = []

        for i in list_off_experiences:
            try:
                name = i.find(
                    'div', {'class': 'display-flex align-items-center mr1 hoverable-link-text t-bold'}).find('span').get_text().strip()
            except:
                try:
                    name = i.find('div', {'class': 'display-flex align-items-center mr1 t-bold'}
                                  ).find('span').get_text().strip()
                except:
                    continue

            current_experience = Experience(name=name)

            try:
                # group of experiences
                group = i.find('ul', {'class': 'pvs-list'})
                elemets = group.find_all('li', {'class': 'pvs-list__paged-list-item pvs-list__item--one-column'})
                for j in elemets:
                    element_name = j.find(
                        'div', {'class': 'display-flex align-items-center mr1 hoverable-link-text t-bold'}).find('span').get_text().strip()

                    try:
                        element_time = j.find('span', {'class': 't-14 t-normal t-black--light'}
                                              ).find('span').get_text().strip()
                    except:
                        element_time = ''

                    try:
                        element_description = j.find(
                            'div', {'class': 'display-flex align-items-center t-14 t-normal t-black'}).find('span').get_text().strip()
                    except:
                        element_description = ''

                    sub_exprecience = Experience(name=element_name, time=element_time, description=element_description)
                    sub_exprecience.group = None
                    current_experience.group.append(sub_exprecience)
            except:
                current_experience.group = None

            if not current_experience.group:
                try:
                    time = i.find('span', {'class': 't-14 t-normal t-black--light'}).find('span').get_text().strip()
                except:
                    time = ''

                current_experience.time = time

                try:
                    element_description = i.find(
                        'div', {'class': 'display-flex align-items-center t-14 t-normal t-black'}).find('span').get_text().strip()
                except:
                    element_description = ''

                current_experience.description = element_description

            profile.experiences.append(current_experience)

        return profile

    @staticmethod
    def get_education(html: str, profile: Profile) -> Profile:
        soup = BeautifulSoup(html, 'lxml')

        try:
            list_off_education = soup.find(
                'ul',
                {'class': 'pvs-list'}
            ).find_all('li', {'class', 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
        except:
            profile.education = []

        for i in list_off_education:
            try:
                name = i.find(
                    'div',
                    {'class': 'display-flex align-items-center mr1 hoverable-link-text t-bold'}
                ).find('span').get_text().strip()
            except:
                continue

            try:
                entity = i.find(
                    'span',
                    {'class': 't-14 t-normal'}
                ).find('span').get_text().strip()
            except:
                entity = ''

            try:
                time = i.find(
                    'span',
                    {'class': 't-14 t-normal t-black--light'}
                ).find('span').get_text().strip()
            except:
                time = ''

            profile.education.append(Education(name=name, entity=entity, time=time))
        return profile

    @staticmethod
    def get_profile_data(username: str, cookie: str, user: User, only_check: bool = False) -> bool:
        service = Service(executable_path=r'/usr/local/bin/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        Linkedin.login_with_cookie(driver, cookie)

        time.sleep(2)
        driver.get(f'https://www.linkedin.com/in/{username}/')
        time.sleep(2)

        if len(driver.page_source) == 39:
            return False, "Ah, it appears there's a slight hiccup with your Token!"

        time.sleep(1)

        if '404' in driver.current_url:
            return False, "By the four Founders! No user hath been unearthed with this username from the depths of our magical archives!"

        if only_check:
            return True

        profile = Linkedin.get_general_info(driver.page_source)
        driver.get(f'https://www.linkedin.com/in/{username}/overlay/contact-info/')
        time.sleep(2)
        profile = Linkedin.get_contact_info(driver.page_source, profile)

        driver.get(f'https://www.linkedin.com/in/{username}/details/certifications/')
        time.sleep(2)
        Linkedin.scroll(driver)
        profile = Linkedin.get_certifications(driver.page_source, profile)

        driver.get(f'https://www.linkedin.com/in/{username}/details/experience/')
        time.sleep(2)
        Linkedin.scroll(driver)
        profile = Linkedin.get_experience(driver.page_source, profile)

        driver.get(f'https://www.linkedin.com/in/{username}/details/education/')
        time.sleep(2)
        Linkedin.scroll(driver)
        profile = Linkedin.get_education(driver.page_source, profile)
        driver.close()

        profile = profile.serrialize()
        try:
            user = UserProfileHtml.objects.get(
                target=username,
                user=user
            )
            user.data = profile
            user.save()
        except UserProfileHtml.DoesNotExist:
            user = UserProfileHtml(
                target=username,
                user=user,
                data=profile
            )
            user.save()

        return True
