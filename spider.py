# Design mock-up: what should a spider look like?
from uf6 import Spider, Option
from uf6 import properties as p, types as t


class MySpider(Spider):

    name = 'my_spider'
    description = ''
    source_label = 'My Service'
    source_url = 'http://my-service.com'
    api_key = Option(description='My Service API Key')
    
    def lookup(self, search_node):
        # Get a node attribute:
        label = search_node.get(p.label)

        # or:
        if not search_node.is_a(t.Company):
            return

        # Some web or database lookup:
        results = self.my_service_search(label)
        for result in results:
            assert isinstance(result, dict)
            result_url = result.get('url')

            # A result context, i.e. a unit of results
            ctx = self.make_context(url=result_url)

            # Make a result node, assert it's the search node
            result_node = ctx.make_node(t.Company)
            result_node.match_for(search_node)

            # Set some attributes:
            result_node.set(p.label, result.get('title'))
            result_node.set(p.address, result.get('postal_address'))

            self.emit(result_node)
