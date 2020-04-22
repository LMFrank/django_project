import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import axios from 'axios'
import BootstrapVue from 'bootstrap-vue'
import VueRouterUserRoles from "vue-router-user-roles";
axios.defaults.baseURL = 'http://52.30.196.202/'
    // axios.defaults.baseURL = 'http://localhost:8000/'

Vue.config.productionTip = false

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(VueRouterUserRoles, { router });
Vue.use(require('vue-moment'));

var filter = function(text, length, clamp) {
    clamp = clamp || '...';
    var node = document.createElement('div');
    node.innerHTML = text;
    var content = node.textContent;
    return content.length > length ? content.slice(0, length) + clamp : content;
};
Vue.filter('truncate', filter);


let getUser = axios.get('/api/me/').then(response => {
    return (response.data)

}).catch(error => {
    console.log(error)
    return ({ role: 'guest' })
});

getUser.then(user => {
    Vue.prototype.$user.set(user);
    new Vue({
        render: h => h(App),
        router,
        store,
        vuetify
    }).$mount("#app");
});