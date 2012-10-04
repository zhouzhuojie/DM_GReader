Data mining tools built upon personal Google Reader
==========

* To generate a "snapshot" like feature of one day's summary.
* To cluster one day's feeds into k groups, focus on users' interests.
* To score the importance of the articles, detect duplication, similarity calculation and other typical data mining tools.



Usage
==========

Example:

    import DM_GReader
    Username = 'foobar@gmail.com'
    Password = 'password'
    dm = DM_GReader(Username, Password)
    dm.import_category()


This will import the remote Google Reader data and dump it to local pickle data for future use.



Credits
==========

This Python package is built upon libgreader and pattern.
