from mailu import models
from mailu.ui import ui, forms, access

import flask
import wtforms_components


@ui.route('/alternative/list/<domain_name>', methods=['GET'])
@access.global_admin
def alternative_list(domain_name):
    domain = models.Domain.query.get(domain_name) or flask.abort(404)
    return flask.render_template('alternative/list.html', domain=domain)


@ui.route('/alternative/create/<domain_name>', methods=['GET', 'POST'])
@access.global_admin
def alternative_create(domain_name):
    domain = models.Domain.query.get(domain_name) or flask.abort(404)
    form = forms.AlternativeForm()
    if form.validate_on_submit():
        conflicting_domain = models.Domain.query.get(form.name.data)
        conflicting_alternative = models.Alternative.query.get(form.name.data)
        conflicting_relay = models.Relay.query.get(form.name.data)
        if conflicting_domain or conflicting_alternative or conflicting_relay:
            flask.flash('Domain %s is already used' % form.name.data, 'error')
        else:
            alternative = models.Alternative(domain=domain)
            form.populate_obj(alternative)
            models.db.session.add(alternative)
            models.db.session.commit()
            flask.flash('Alternative domain %s created' % alternative)
            return flask.redirect(
                flask.url_for('.alternative_list', domain_name=domain.name))
    return flask.render_template('alternative/create.html',
        domain=domain, form=form)


@ui.route('/alternative/delete/<alternative>', methods=['GET', 'POST'])
@access.global_admin
@access.confirmation_required("delete {alternative}")
def alternative_delete(alternative):
    alternative = models.Alternative.query.get(alternative) or flask.abort(404)
    domain = alternative.domain
    models.db.session.delete(alternative)
    models.db.session.commit()
    flask.flash('Alternative %s deleted' % alternative)
    return flask.redirect(
        flask.url_for('.alternative_list', domain_name=domain.name))


@ui.route('/alternative/<alternative>/check/mx', methods=['GET'])
@access.domain_admin(models.Alternative, 'alternative')
def alternative_check_mx(alternative):
    alternative = models.Alternative.query.get(alternative) or flask.abort(404)
    result = alternative.check_mx()
    return flask.redirect("/static/success.png" if result else "/static/failed.png")


@ui.route('/alternative/<alternative>/check/spf', methods=['GET'])
@access.domain_admin(models.Alternative, 'alternative')
def alternative_check_spf(alternative):
    alternative = models.Alternative.query.get(alternative) or flask.abort(404)
    result = alternative.check_spf()
    return flask.redirect("/static/success.png" if result else "/static/failed.png")


@ui.route('/alternative/<alternative>/check/dkim', methods=['GET'])
@access.domain_admin(models.Alternative, 'alternative')
def alternative_check_dkim(alternative):
    alternative = models.Alternative.query.get(alternative) or flask.abort(404)
    result = alternative.check_dkim()
    return flask.redirect("/static/success.png" if result else "/static/failed.png")


@ui.route('/alternative/<alternative>/check/dmarc', methods=['GET'])
@access.domain_admin(models.Alternative, 'alternative')
def alternative_check_dmarc(alternative):
    alternative = models.Alternative.query.get(alternative) or flask.abort(404)
    result = alternative.check_dmarc()
    return flask.redirect("/static/success.png" if result else "/static/failed.png")


@ui.route('/alternative/<alternative>/check/dmarcreport', methods=['GET'])
@access.domain_admin(models.Alternative, 'alternative')
def alternative_check_dmarc_report(alternative):
    alternative = models.Alternative.query.get(alternative) or flask.abort(404)
    result = alternative.check_dmarc_report()
    return flask.redirect("/static/success.png" if result else "/static/failed.png")

