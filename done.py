import string
from unicodedata import name
import requests
import json
import re

courseIdRx = re.compile("data-clp-course-id=\"(\d+)\"")

session = requests.Session()
session.cookies.update(
    {'access_token': 'xxxxxxxxxxxxxxxxx'}) #get it from browser cookies


def getLectures(courseID):
    params = (
        ('page_size', '3000'),
    )

    lecturesResponse = session.get(
        f'https://www.udemy.com/api-2.0/courses/{courseID}/subscriber-curriculum-items/', params=params)
    return lecturesResponse.json()


def markAll(courseID, course: json):
    json_data = {
        'lecture_id': 20205174,
        'downloaded': False,
    }

    for entity in course['results']:
        if entity['_class'] == 'lecture':
            json_data['lecture_id'] = entity['id']
            response = session.post(
                        f'https://www.udemy.com/api-2.0/users/me/subscribed-courses/{courseID}/completed-lectures/', json=json_data)
            if response.status_code == 201:
                print(f"Marked {entity['title']}")
            else:
                print(response.status_code, response.text)

def getCourseID(url: string):
    response = session.get(url)
    courseID = courseIdRx.search(response.text).group(1)
    return courseID

if __name__ == "__main__":
    courseURL = input("Enter the course URL:")
    courseID = getCourseID(courseURL)
    lectures = getLectures(courseID)
    #print(lectures)
    markAll(courseID, lectures)

