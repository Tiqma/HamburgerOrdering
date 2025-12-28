#!/usr/bin/env python3
"""Tests for models"""
import unittest
from app import create_app, db
from app.models import User, Burger, Ingredient, BurgerIngredient
from flask import current_app
class ModelTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test context and database"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def testCreateUser(self):
        """Test user creation"""
        user = User(username='testuser', email='test@mail.com', full_name='Olle')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        queried_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.email, 'test@mailx.com')

    def tearDown(self):
        """Tear down test context and database"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()