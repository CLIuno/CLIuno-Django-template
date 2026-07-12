from src.models import Post
from src.tests.base import BaseTestCase


class PostCRUDTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(
            title='Test Post', content='Test Content', user=self.user
        )

    def test_get_all_posts(self):
        resp = self.client.get('/api/v1/posts/', **self.auth_header())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['data']['posts']), 1)

    def test_get_post_by_id(self):
        resp = self.client.get(
            f'/api/v1/posts/{self.post.id}', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['post']['title'], 'Test Post')

    def test_get_post_not_found(self):
        import uuid
        resp = self.client.get(
            f'/api/v1/posts/{uuid.uuid4()}', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 404)

    def test_create_post(self):
        resp = self.client.post(
            '/api/v1/posts/create',
            {'title': 'New Post', 'content': 'New Content'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['result']['title'], 'New Post')

    def test_create_post_missing_fields(self):
        resp = self.client.post(
            '/api/v1/posts/create',
            {'title': 'No content'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 400)

    def test_update_post(self):
        resp = self.client.patch(
            f'/api/v1/posts/{self.post.id}/update',
            {'title': 'Updated Title'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_delete_post(self):
        resp = self.client.delete(
            f'/api/v1/posts/{self.post.id}/delete', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_get_current_user_posts(self):
        resp = self.client.get(
            '/api/v1/posts/current-user', **self.auth_header())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['data']['posts']), 1)

    def test_no_auth(self):
        resp = self.client.get('/api/v1/posts/')
        self.assertEqual(resp.status_code, 401)


class CommentTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(
            title='Test Post', content='Test Content', user=self.user
        )

    def test_create_comment(self):
        resp = self.client.post(
            f'/api/v1/posts/{self.post.id}/comments/create',
            {'content': 'Nice post!'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['data']
                         ['comment']['content'], 'Nice post!')

    def test_get_comments(self):
        from src.models import Comment
        Comment.objects.create(content='Comment 1',
                               user=self.user, post=self.post)
        resp = self.client.get(
            f'/api/v1/posts/{self.post.id}/comments', **self.auth_header()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['data']['comments']), 1)

    def test_update_own_comment(self):
        from src.models import Comment
        comment = Comment.objects.create(
            content='Original', user=self.user, post=self.post
        )
        resp = self.client.patch(
            f'/api/v1/posts/{self.post.id}/comments/{comment.id}/update',
            {'content': 'Edited'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['comment']['content'], 'Edited')

    def test_delete_own_comment(self):
        from src.models import Comment
        comment = Comment.objects.create(
            content='Delete me', user=self.user, post=self.post
        )
        resp = self.client.delete(
            f'/api/v1/posts/{self.post.id}/comments/{comment.id}/delete',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 200)

    def test_cannot_update_others_comment(self):
        from src.models import Comment
        comment = Comment.objects.create(
            content='Admin comment', user=self.admin_user, post=self.post
        )
        resp = self.client.patch(
            f'/api/v1/posts/{self.post.id}/comments/{comment.id}/update',
            {'content': 'Hacked'},
            content_type='application/json',
            **self.auth_header(),
        )
        self.assertEqual(resp.status_code, 403)
