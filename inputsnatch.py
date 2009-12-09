#!/usr/bin/python

class InputSnatcher:
    def __init__(self,url=None):
        self.url = url # where we are going to scrape
        self.post_params = None # if we see these than we are going to post
        self.method = 'POST' if self.post_params else 'GET'
        self.forms = [] # the result of our scrape
        self.data = {} # dict of our inputs

    def scrape(self):
        import urllib2
        if self.post_params:
            import urllib
            result = urllib2.urlopen(self.url,
                                     urllib.urlencode(self.post_params))
        else:
            result = urllib2.urlopen(self.url)
        lines = result.readlines()

        import BeautifulSoup
        soup = BeautifulSoup.BeautifulSoup(''.join(lines))

        # now that we have our html, lets try to grab up all the inputs
        # grouped by form
        for form in soup.findAll('form'):
            inputs = self._parse_inputs(form)
            details = self._parse_details(form)
            details['url'] = self.url
            self.forms.append([details,inputs]) # using a list so it's jsonable

        return self.forms

    def _parse_details(self,piece):
        to_return = {}
        for k,v in piece.attrs:
            to_return[k] = v
        return to_return

    def _parse_inputs(self,form):
        # won't always be this easy
        inputs = [self._parse_details(i) for i in form.findAll('input')]
        buttons = [self._parse_details(b) for b in form.findAll('button')]
        submits = [self._parse_details(s) for s in form.findAll('submit')]
        return inputs + buttons + submits # simple for now


if __name__ == '__main__':
    # parse our args
    from optparse import OptionParser
    option_parser = OptionParser()
    option_parser.usage = "%prog [options] form_url ..."
    option_parser.description = "Will scrape the given url for forms / inputs"
    option_parser.add_option('--sectionname', dest='section_template',
                             help="define a template for the section names")
    options, args = option_parser.parse_args()

    # set the template we are going to use form our names
    section_name_template = options.section_template or 'form_%(url)s_%(action)s'

    print "url:",args

    # grab an input snatcher, scrape the form
    snatcher = InputSnatcher(args[0])
    forms = snatcher.scrape()
    data = {}

    for form in forms:
        params = { 'url':'', 'action':'' }
        params.update(form[0])
        section_name = section_name_template % params
        for input in form[1]:
            data.setdefault(section_name,[]).append(input)


    import json
    print json.dumps(data)





