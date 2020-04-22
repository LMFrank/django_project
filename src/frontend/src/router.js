import Vue from 'vue'
import Router from 'vue-router'
import Books from './views/Books.vue'
import BookDetail from './views/BookDetail.vue'
import Category from './views/Category.vue'
import Author from './views/Author.vue'

import CategoryDetail from './views/CategoryDetail.vue'
import AuthorDetail from './views/AuthorDetail.vue'


Vue.use(Router)

let router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [

        {
            path: '/books',
            name: 'books',
            component: Books,
            meta: {
                title: 'Book'
            }
        },
        {
            path: '/books/:id',
            name: 'bookDetail',
            component: BookDetail,
            meta: {
                title: 'Book | Details'
            }
        },
        {
            path: '/category',
            name: 'category',
            component: Category,
            meta: {
                title: 'Category'
            }
        },
        {
            path: '/category/:id',
            name: 'CategoryDetail',
            component: CategoryDetail,
            meta: {
                title: 'Category | Details'
            }
        },
        {
            path: '/author',
            name: 'Authors',
            component: Author,
            meta: {
                title: 'Author'
            }
        },
        {
            path: '/author/:id',
            name: 'AuthorDetail',
            component: AuthorDetail,
            meta: {
                title: 'Author | Details'
            }
        },
        {
            path: '/',
            redirect: '/books'
        },
    ]
})


export default router;