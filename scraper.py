import requests
from bs4 import BeautifulSoup
import json
import os
import time

def scrape_su():
    # ALL YOUR COLLECTED URLs
    urls = [
        "https://www.cardiffstudents.com/",
        "https://www.cardiffstudents.com/whatson/all/",
        "https://www.cardiffstudents.com/whatson/live-music/",
        "https://www.cardiffstudents.com/whatson/bars-club/",
        "https://www.cardiffstudents.com/our-venues/venue-hire/",
        "https://www.cardiffstudents.com/our-venues/venue-hire/meeting-rooms/",
        "https://www.cardiffstudents.com/our-venues/venue-hire/conferences/",
        "https://www.cardiffstudents.com/our-venues/venue-hire/exhibitions-events/",
        "https://www.cardiffstudents.com/our-venues/venue-hire/dinners-parties/",
        "https://www.cardiffstudents.com/our-venues/venue-hire/filming-locations/",
        "https://www.cardiffstudents.com/our-venues/events/",
        "https://www.cardiffstudents.com/our-venues/events/yolo/",
        "https://www.cardiffstudents.com/our-venues/events/circle/",
        "https://www.cardiffstudents.com/our-venues/events/live-music/",
        "https://www.cardiffstudents.com/our-venues/events/pub-events/",
        "https://www.cardiffstudents.com/our-venues/eat-and-drink/",
        "https://www.cardiffstudents.com/our-venues/eat-and-drink/taf/",
        "https://www.cardiffstudents.com/our-venues/eat-and-drink/yplascwtch/",
        "https://www.cardiffstudents.com/about-cusu/app/",
        "https://www.cardiffstudents.com/our-venues/accessibility-and-safety/",
        "https://www.cardiffstudents.com/our-venues/accessibility-and-safety/safety-in-our-venues/",
        "https://www.cardiffstudents.com/about/contact-us/",
        "https://www.cardiffstudents.com/about/contact-us/meet-the-team/",
        "https://www.cardiffstudents.com/about/contact-us/stay-in-touch/",
        "https://www.cardiffstudents.com/about/visit-us/",
        "https://www.cardiffstudents.com/about/visit-us/open-days/",
        "https://www.cardiffstudents.com/about/visit-us/open-spaces/",
        "https://www.cardiffstudents.com/about/advertise/",
        "https://www.cardiffstudents.com/about/advertise/book-with-us/",
        "https://www.cardiffstudents.com/about/advertise/fairs/",
        "https://www.cardiffstudents.com/about/advertise/our-spaces/",
        "https://www.cardiffstudents.com/about/hwr/",
        "https://www.cardiffstudents.com/about/hwr/reports-and-policy/",
        "https://cardiffstudents.my.canva.site/impact-report-25",
        "https://www.cardiffstudents.com/about/hwr/work-with-us/",
        "https://www.cardiffstudents.com/about/hwr/privacy/",
        "https://www.cardiffstudents.com/about/hwr/our-strategy/",
        "https://www.cardiffstudents.com/about/cymraeg/",
        "https://cardiffstudents.my.canva.site/50-years",
        "https://www.cardiffstudents.com/whatson/giveitago/",
        "https://www.cardiffstudents.com/whatson/society-club/",
        "https://www.cardiffstudents.com/whatson/postgrad/",
        "https://www.cardiffstudents.com/whatson/international/",
        "https://www.cardiffstudents.com/whatson/heath/",
        "https://www.cardiffstudents.com/activities/",
        "https://www.cardiffstudents.com/activities/au/",
        "https://www.cardiffstudents.com/activities/societies/",
        "https://www.cardiffstudents.com/your-voice/networks/",
        "https://www.cardiffstudents.com/your-voice/reps/",
        "https://www.cardiffstudents.com/your-voice/reps/become-a-rep/",
        "https://www.cardiffstudents.com/your-voice/reps/resources/",
        "https://www.cardiffstudents.com/your-voice/reps/college/",
        "https://www.cardiffstudents.com/your-voice/reps/fforwm/",
        "https://www.cardiffstudents.com/your-voice/democracy/",
        "https://www.cardiffstudents.com/your-voice/democracy/agm/",
        "https://www.cardiffstudents.com/your-voice/democracy/senate/",
        "https://www.cardiffstudents.com/your-voice/democracy/executivecommittees/",
        "https://www.cardiffstudents.com/your-voice/democracy/accountability/",
        "https://www.cardiffstudents.com/your-voice/democracy/policy/",
        "https://www.cardiffstudents.com/your-voice/democracy/policy/ideas/",
        "https://www.cardiffstudents.com/your-voice/democracy/referenda/",
        "https://www.cardiffstudents.com/election-takeover/",
        "https://www.cardiffstudents.com/your-voice/campaigns/",
        "https://www.cardiffstudents.com/your-voice/elected-officers/",
        "https://www.cardiffstudents.com/your-voice/elected-officers/student-wins/",
        "https://www.cardiffstudents.com/your-voice/international-students/",
        "https://www.cardiffstudents.com/your-voice/international-students/living-in-cardiff/",
        "https://www.cardiffstudents.com/your-voice/international-students/academic-support/",
        "https://www.cardiffstudents.com/your-voice/international-students/global-campus/",
        "https://www.cardiffstudents.com/your-voice/elected-officers/archive/",
        "https://www.cardiffstudents.com/your-voice/heath-park/",
        "https://www.cardiffstudents.com/your-voice/heath-park/useful-info/",
        "https://www.cardiffstudents.com/your-voice/heath-park/clubs-societies/",
        "https://www.cardiffstudents.com/your-voice/heath-park/placement-support/",
        "https://www.cardiffstudents.com/activities/studentmedia/",
        "https://www.cardiffstudents.com/activities/transport/",
        "https://www.cardiffstudents.com/jobs-skills/training-opportunities/",
        "https://www.cardiffstudents.com/jobs-skills/jobshop/",
        "https://www.cardiffstudents.com/jobs-skills/jobshop/students/",
        "https://www.cardiffstudents.com/jobs-skills/jobshop/staff/",
        "https://www.cardiffstudents.com/jobs-skills/jobshop/employers/",
        "https://www.cardiffstudents.com/jobs-skills/welcometeam/",
        "https://www.cardiffstudents.com/activities/finance-general-services/",
        "https://www.cardiffstudents.com/your-voice/",
        "https://www.cardiffstudents.com/advice/",
        "https://www.cardiffstudents.com/advice/emergencyinformation/",
        "https://www.cardiffstudents.com/advice/academic/",
        "https://www.cardiffstudents.com/advice/academic/academic-appeals/",
        "https://www.cardiffstudents.com/advice/academic/AcademicMisconduct/",
        "https://www.cardiffstudents.com/advice/academic/extenuatingcircumstances/",
        "https://www.cardiffstudents.com/advice/academic/fitnesstopractise/",
        "https://www.cardiffstudents.com/advice/academic/student-conduct/",
        "https://www.cardiffstudents.com/advice/health-and-wellbeing/",
        "https://www.cardiffstudents.com/advice/health-and-wellbeing/alcoholanddrugs/",
        "https://www.cardiffstudents.com/advice/health-and-wellbeing/bullyingandharrassment/",
        "https://www.cardiffstudents.com/advice/health-and-wellbeing/mental-health/",
        "https://www.cardiffstudents.com/advice/health-and-wellbeing/sexual-health/",
        "https://www.cardiffstudents.com/advice/health-and-wellbeing/personalandrelationshipproblems/",
        "https://www.cardiffstudents.com/advice/housing/",
        "https://www.cardiffstudents.com/advice/housing/finding/",
        "https://www.cardiffstudents.com/advice/housing/signing/",
        "https://www.cardiffstudents.com/advice/housing/living/",
        "https://www.cardiffstudents.com/advice/housing/leaving/",
        "https://www.cardiffstudents.com/advice/complaints/",
        "https://www.cardiffstudents.com/advice/complaints/studentsunion/",
        "https://www.cardiffstudents.com/advice/complaints/university/",
        "https://www.cardiffstudents.com/advice/student-life/",
        "https://www.cardiffstudents.com/our-venues/"
    ]

    # Added headers to look like a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    all_data = []
    
    print(f"Starting massive scrape of {len(urls)} pages...")
    
    for i, url in enumerate(urls):
        try:
            print(f"[{i+1}/{len(urls)}] Scraping: {url}...")
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Remove scripts and styles before getting text
                for script in soup(["script", "style"]):
                    script.decompose()
                
                content = soup.get_text(separator=' ', strip=True)
                all_data.append({
                    "url": url,
                    "content": content
                })
            else:
                print(f"   ! Failed: Status {response.status_code}")

            # Politeness delay
            time.sleep(1)

        except Exception as e:
            print(f"   ! Error with {url}: {e}")

    # Save the output
    os.makedirs('data', exist_ok=True)
    with open('data/raw_su_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4)
        
    print(f"\n--- SUCCESS ---")
    print(f"Total pages captured: {len(all_data)}")
    print(f"Data saved to data/raw_su_data.json")

if __name__ == "__main__":
    scrape_su()