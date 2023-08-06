# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deprecate_cmsplugin_filer', 'deprecate_cmsplugin_filer.migrations']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deprecate-cmsplugin-filer',
    'version': '0.1.0',
    'description': 'A small app with a migration for converting deprecated cmsplugin-filer objects to djangocms plugin objects.',
    'long_description': "# deprecate_cmsplugin_filer\nA small app with a migration for converting deprecated cmsplugin-filer objects to djangocms plugin objects. Adapted from https://gist.github.com/wfehr/86ac31e8e263b872b746cc721662251e to add link and video plugin capability.\n\nThings you'll want to evaluate before migrating:\n\n- Whether any custom project-level templates are in use for the cmsplugin filer modules. Any special customizations may need to be re-implemented in the djangocms-[file/link/picture/video] templates.\n\n- If you currently are using django config settings such as CMSPLUGIN_FILER_IMAGE_STYLE_CHOICES or FILER_LINK_STYLES, you'll need to copy these as DJANGOCMS_PICTURE_TEMPLATES and DJANGOCMS_LINK_TEMPLATES, respectively. Note: there is a difference in behavior with FILER_LINK_STYLES and DJANGOCMS_LINK_TEMPLATES. The former would simply set a class while the latter expects a corresponding template to be created. Reference: https://github.com/divio/djangocms-link/#configuration\n\nMigration steps:\n\n1. Before running the migration, you can run the following command to make sure you back up the old plugin tables for quick restoring if needed.\n./manage.py dumpdata cmsplugin_filer_file cmsplugin_filer_folder cmsplugin_filer_image cmsplugin_filer_link cmsplugin_filer_video > ~/cmsplugin_filer.json\n\n2. Ensure you've installed the new plugins, added them to INSTALLED_APPS, and migrated:\npip install djangocms-file djangocms-link djangocms-picture djangocms-video\nINSTALLED_APPS += (\n    'djangocms_file',\n    'djangocms_link',\n    'djangocms_picture',\n    'djangocms_video',\n)\n./manage.py migrate\n\n3. I recommend also running the following command before and after the migration to get an inventory of the site's plugins and ensure they've all been migrated.\n./manage.py cms list plugins\n\n4. Now the small app with the migration can be installed and run:\n./manage.py migrate deprecate_cmsplugin_filer\n\n5. If you once again run ./manage.py cms list plugins, you should see the cmsplugin-filer objects have been converted to djangocms-[file/link/picture/video] objects.\n\n6. Do a spotcheck of plugins on the site. This is where you may see errors related to previous FILER_LINK_STYLES that are now expecting corresponding templates to be created for each style.\n",
    'author': 'Imagescape',
    'author_email': 'info@imagescape.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ImaginaryLandscape/deprecate_cmsplugin_filer',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
