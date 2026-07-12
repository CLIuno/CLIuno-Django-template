from src.models import Follow, User
from src.tests.base import BaseTestCase


class FollowTest(BaseTestCase):
    def test_follow_user(self):
        resp = self.client.post(
            f'/api/v1/follows/{self.admin_user.id}/follow', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(
            Follow.objects.filter(
                follower=self.user, following=self.admin_user
            ).exists()
        )

    def test_follow_self(self):
        resp = self.client.post(
            f'/api/v1/follows/{self.user.id}/follow', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 400)

    def test_follow_duplicate(self):
        Follow.objects.create(follower=self.user, following=self.admin_user)
        resp = self.client.post(
            f'/api/v1/follows/{self.admin_user.id}/follow', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 400)

    def test_unfollow(self):
        Follow.objects.create(follower=self.user, following=self.admin_user)
        resp = self.client.delete(
            f'/api/v1/follows/{self.admin_user.id}/follow', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)

    def test_unfollow_not_following(self):
        resp = self.client.delete(
            f'/api/v1/follows/{self.admin_user.id}/follow', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 404)

    def test_get_followers(self):
        Follow.objects.create(follower=self.user, following=self.admin_user)
        resp = self.client.get(
            f'/api/v1/follows/{self.admin_user.id}/followers', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['data']['followers']), 1)

    def test_get_following(self):
        Follow.objects.create(follower=self.user, following=self.admin_user)
        resp = self.client.get(
            f'/api/v1/follows/{self.user.id}/following', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['data']['following']), 1)

    def test_is_following_true(self):
        Follow.objects.create(follower=self.user, following=self.admin_user)
        resp = self.client.get(
            f'/api/v1/follows/{self.admin_user.id}/is-following',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['data']['isFollowing'])

    def test_is_following_false(self):
        resp = self.client.get(
            f'/api/v1/follows/{self.admin_user.id}/is-following',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.json()['data']['isFollowing'])
