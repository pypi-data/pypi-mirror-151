import unittest
from django.urls import reverse
from django.test import Client
from .models import Driver, DriverStep
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_driver(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["slug"] = "slug"
    defaults["className"] = "className"
    defaults["animate"] = "animate"
    defaults["opacity"] = "opacity"
    defaults["padding"] = "padding"
    defaults["allowClose"] = "allowClose"
    defaults["overlayClickNext"] = "overlayClickNext"
    defaults["doneBtnText"] = "doneBtnText"
    defaults["closeBtnText"] = "closeBtnText"
    defaults["stageBackground"] = "stageBackground"
    defaults["nextBtnText"] = "nextBtnText"
    defaults["prevBtnText"] = "prevBtnText"
    defaults["showButtons"] = "showButtons"
    defaults["keyboardControl"] = "keyboardControl"
    defaults["scrollIntoViewOptions"] = "scrollIntoViewOptions"
    defaults["onHighlightStarted"] = "onHighlightStarted"
    defaults["onHighlighted"] = "onHighlighted"
    defaults["onDeselected"] = "onDeselected"
    defaults["onReset"] = "onReset"
    defaults["onNext"] = "onNext"
    defaults["onPrevious"] = "onPrevious"
    defaults.update(**kwargs)
    return Driver.objects.create(**defaults)


def create_driverstep(**kwargs):
    defaults = {}
    defaults["element"] = "element"
    defaults["stageBackground"] = "stageBackground"
    defaults["className"] = "className"
    defaults["title"] = "title"
    defaults["description"] = "description"
    defaults["showButtons"] = "showButtons"
    defaults["doneBtnText"] = "doneBtnText"
    defaults["closeBtnText"] = "closeBtnText"
    defaults["nextBtnText"] = "nextBtnText"
    defaults["prevBtnText"] = "prevBtnText"
    defaults["onNext"] = "onNext"
    defaults["onPrevious"] = "onPrevious"
    defaults.update(**kwargs)
    if "driver" not in defaults:
        defaults["driver"] = create_driver()
    return DriverStep.objects.create(**defaults)


class DriverViewTest(unittest.TestCase):
    '''
    Tests for Driver
    '''
    def setUp(self):
        self.client = Client()

    def test_list_driver(self):
        url = reverse('Driverjs_driver_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_driver(self):
        url = reverse('Driverjs_driver_create')
        data = {
            "name": "name",
            "slug": "slug",
            "className": "className",
            "animate": "animate",
            "opacity": "opacity",
            "padding": "padding",
            "allowClose": "allowClose",
            "overlayClickNext": "overlayClickNext",
            "doneBtnText": "doneBtnText",
            "closeBtnText": "closeBtnText",
            "stageBackground": "stageBackground",
            "nextBtnText": "nextBtnText",
            "prevBtnText": "prevBtnText",
            "showButtons": "showButtons",
            "keyboardControl": "keyboardControl",
            "scrollIntoViewOptions": "scrollIntoViewOptions",
            "onHighlightStarted": "onHighlightStarted",
            "onHighlighted": "onHighlighted",
            "onDeselected": "onDeselected",
            "onReset": "onReset",
            "onNext": "onNext",
            "onPrevious": "onPrevious",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_driver(self):
        driver = create_driver()
        url = reverse('Driverjs_driver_detail', args=[driver.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_driver(self):
        driver = create_driver()
        data = {
            "name": "name",
            "slug": "slug",
            "className": "className",
            "animate": "animate",
            "opacity": "opacity",
            "padding": "padding",
            "allowClose": "allowClose",
            "overlayClickNext": "overlayClickNext",
            "doneBtnText": "doneBtnText",
            "closeBtnText": "closeBtnText",
            "stageBackground": "stageBackground",
            "nextBtnText": "nextBtnText",
            "prevBtnText": "prevBtnText",
            "showButtons": "showButtons",
            "keyboardControl": "keyboardControl",
            "scrollIntoViewOptions": "scrollIntoViewOptions",
            "onHighlightStarted": "onHighlightStarted",
            "onHighlighted": "onHighlighted",
            "onDeselected": "onDeselected",
            "onReset": "onReset",
            "onNext": "onNext",
            "onPrevious": "onPrevious",
        }
        url = reverse('Driverjs_driver_update', args=[driver.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class DriverStepViewTest(unittest.TestCase):
    '''
    Tests for DriverStep
    '''
    def setUp(self):
        self.client = Client()

    def test_list_driverstep(self):
        url = reverse('Driverjs_driverstep_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_driverstep(self):
        url = reverse('Driverjs_driverstep_create')
        data = {
            "element": "element",
            "stageBackground": "stageBackground",
            "className": "className",
            "title": "title",
            "description": "description",
            "showButtons": "showButtons",
            "doneBtnText": "doneBtnText",
            "closeBtnText": "closeBtnText",
            "nextBtnText": "nextBtnText",
            "prevBtnText": "prevBtnText",
            "onNext": "onNext",
            "onPrevious": "onPrevious",
            "driver": create_driver().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_driverstep(self):
        driverstep = create_driverstep()
        url = reverse('Driverjs_driverstep_detail', args=[driverstep.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_driverstep(self):
        driverstep = create_driverstep()
        data = {
            "element": "element",
            "stageBackground": "stageBackground",
            "className": "className",
            "title": "title",
            "description": "description",
            "showButtons": "showButtons",
            "doneBtnText": "doneBtnText",
            "closeBtnText": "closeBtnText",
            "nextBtnText": "nextBtnText",
            "prevBtnText": "prevBtnText",
            "onNext": "onNext",
            "onPrevious": "onPrevious",
            "driver": create_driver().pk,
        }
        url = reverse('Driverjs_driverstep_update', args=[driverstep.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


