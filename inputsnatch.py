

class InputSnatcher:
    def __init__(self,url=None):
        self.url = url # where we are going to scrape
        self.post_params = None # if we see these than we are going to post
        self.method = 'POST' if self.post_params else 'GET'

    def scrape(self):
        import urllib2
        if self.post_params:
            import urllib
            result = urllib2.urlopen(self.url,
                                     urllib.urlencode(self.post_params))
        else:
            result = urllib2.urlopen(self.url)
        lines = result.getlines()

        import BeautifulSoup
        soup = BeautifulSoup.BeautifulSoup(''.join(lines))

        # now that we have our html, lets try to grab up all the inputs
        # grouped by form
        for form in soup.findAll('form'):
            inputs = this.get_inputs(form)


    def get_inputs(form):
        # won't always be this easy
        inputs = [x for x in form.findAll('input')]
        buttons = [x for x in form.findAll('button')]
        submits = [x for x in form.findAll('submit')]
        return inputs + buttons + submits # simple for now
