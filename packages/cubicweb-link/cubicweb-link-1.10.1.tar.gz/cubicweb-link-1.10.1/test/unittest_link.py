# -*- coding: utf-8 -*-
from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.web.views import uicfg, actions

from cubicweb_link import views

afs = uicfg.autoform_section


class LinkTC(CubicWebTC):

    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity('Link', title=u"vous êtes perdu ?", url=u"http://www.perdu.com")
            cnx.commit()

    def test_possible_actions(self):
        with self.admin_access.web_request() as req:
            rset = req.execute('Any X WHERE X is Link')
            allactions = self.pactionsdict(req, rset)
            self.assertEqual(allactions['mainactions'],
                             [actions.ModifyAction,
                              views.LinkFollowAction])
            self.assertEqual(allactions['moreactions'],
                             [actions.ManagePermissionsAction,
                              actions.AddRelatedActions,
                              actions.DeleteAction,
                              actions.CopyAction,
                              ])

    def test_relations_by_category(self):
        def rbc(iterable):
            return [(rschema.type, x) for rschema, tschemas, x in iterable]
        with self.admin_access.web_request() as req:
            e = self.vreg["etypes"].etype_class('Link')(req)
            self.assertEqual(rbc(afs.relations_by_section(e, 'main', 'attributes', 'update')),
                             [('title', 'subject'), ('url', 'subject'),
                              ('description', 'subject')])
        with self.admin_access.repo_cnx() as cnx:
            self.create_user(cnx, u'toto')
        with self.new_access(u'toto').web_request() as req:
            # create a new instance with the new connection
            e = self.vreg["etypes"].etype_class('Link')(req)
            self.assertEqual(rbc(afs.relations_by_section(e, 'main', 'attributes', 'update')),
                             [('title', 'subject'), ('url', 'subject'),
                              ('description', 'subject')])


if __name__ == '__main__':
    from unittest import main
    main()
