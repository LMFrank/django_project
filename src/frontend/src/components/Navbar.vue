<template>
  <div>
    <v-app-bar app flat>
      <v-app-bar-nav-icon @click="drawer=!drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>Library <span>(Using DRF & Vue)</span></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="warning" @click="template">Check out templates implementation</v-btn>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" app disable-route-watcher>
      <v-list-item>
        <v-list-item-avatar>
          <v-badge>
            <v-icon large>mdi-library</v-icon>
          </v-badge>
        </v-list-item-avatar>

        <v-list-item-title>{{$user.get().username}}</v-list-item-title>
      </v-list-item>

      <v-divider></v-divider>
      <v-list dense nav>
        <v-list-item v-for="item in items" :key="item.title" link v-bind:to="item.to">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click="login" link v-if="$user.get().role == 'guest'">
          <v-list-item-icon>
            <v-icon>mdi-login</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Login</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click="logout" link v-else>
          <v-list-item-icon>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>



<script>
import axios from "axios";
export default {
  data() {
    return {
      drawer: true,
      user: {},
      items: [
        { title: "Books", icon: "mdi-book-multiple", to: "/books" },
        { title: "Auhtors", icon: "mdi-pen", to: "/author" },
        {
          title: "Categories",
          icon: "mdi-format-list-bulleted-type",
          to: "/category"
        }
      ],
      mini: true,
      right: null
    };
  },
  methods: {
    logout: function() {
      window.location.href = "/logout/";
    },
    login: function() {
      window.location.href = "/login/";
    },
    template : function () { 
      window.location.href = "/t/books/";

    }
  },
  mounted() {}
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
