from twill import get_browser
import unittest
import re

sites = {
    'plus' : 'http://plus.the-hub.net/',
    'psn' : 'http://psychosocialnetwork.net/',
    'plus_dev' : 'http://plusdev-app.the-hub.net:8000/',
    'psn_dev' : 'http://plusdev-app.the-hub.net:1999/',
    }

reg = re.compile("DEBUG_STATUS=OK")
browser = get_browser()

areas = ['explore','members','groups','hubs','regions']


class TestSites(unittest.TestCase) :
    pass

def add_test(cls,site,url) :
    def test_it(self) :
        print
        print site, url
        browser.go(url)
        self.assertEquals(browser.get_code(),200)
        print "testing debug_status"
        self.assertTrue(reg.search(browser.get_html()))
        for area in areas :
            browser.go('%s%s/' % (url,area))
            self.assertTrue(reg.search(browser.get_html()))
        browser.go('%s%s/%s'%(url,'groups',1))
        self.assertTrue(reg.search(browser.get_html()))
                 

    setattr(cls,'test_%s'%site,test_it)

for site,url in sites.iteritems() :
    add_test(TestSites,site,url)
    reg = re.compile("DEBUG_STATUS=OK")

if __name__ == '__main__' :
    unittest.main()
