# springserve-python
Python Library for accessing the Springserve API

Installation
-------------

To install from source:

    python setup.py install 

To install from pip:

    pip install springserve 
  
Usage
-----------

### Configuration ###

Springserve is using link to handle it's configuration.  Link is a way to
centrally configure your database, api handles. It has support for Springserve
api connections.  For more, see the link documentation.  https://link-docs.readthedocs.org/en/latest/

Link will be installed when you install springserve

To configure link for springserve:

Open ipython and run the following. This will edit your link.config.  By default this will be ~/.link/link.config.  
You can change this directory location by setting the environment variable  LNK_DIR

Here is an example config:
		
		In [1]: import springserve

		In [2]: springserve.setup_config()
		Enter a user name: optimization@springserve.com
		Enter password:
		Would you like write[Y/n] y
		writing config to: /Users/{username}/.link/link.config
		done: refreshing config

### Tab Completion and IPython ###

The python library was built to work seamlessly with tools like IPython. IPython
is an interactive shell that is well suited for adhoc data analysis as well as
general python debugging. One of it's best features is tab completion and
documentation
	
		In [1]: import springserve as sprg

		In [2]: sprg.<tab>

			sprg.API    sprg.demand_tags   sprg.domain_lists  sprg.raw_get sprg.supply_tags
		
		# see documentation on the get function of supply_tags
		In [3]: sprg.supply_tags.get?

		Type:        instancemethod
		String form: <bound method _SupplyTagAPI.get of
		<springserve._supply._SupplyTagAPI object at 0x103439ad0>>
		File:        /Users/dave/src/springserve-python/springserve/__init__.py
		Definition:  sprg.supply_tags.get(self, path_param=None, query_params=None)
		Docstring:   used to call the /supply_tags end point...more docs to come

		# get a supply_tag by it's id
		In [4]: tag = sprg.supply_tags.get(1234)		
		
		# see what fields exist on the supply_tag
		In [5]: tag.<tab>

		tag.active                 tag.domain_list_ids        tag.player_size_targeting
		tag.supply_partner_id
		tag.allowed_player_sizes   tag.domain_targeting       tag.rate
		tag.supply_type
		tag.country_codes          tag.id                     tag.raw
		tag.country_targeting      tag.name                   tag.save
		tag.demand_tag_priorities  tag.payment_terms          tag.supply_group_id

		# see the contents of a field
		In [5]: tag.name
		Out[7]: "My Test Tag"
		
		# change the contents and save it
		In [6]: tag.name = "My New Test Tag"
		In [7]: resp = tag.save()

In addition to working with single responses.  This simple interface makes it
easy to make calls that will return more than one result.
		

		In [8]: tags = sprg.demand_tags.get()

		In [9]: for tag in tags:
		...:     print tag.name
		...:

		My Tag 1	
		My Tag 2
		
