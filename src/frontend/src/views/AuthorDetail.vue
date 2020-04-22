<template>
  <v-container>
    <v-layout row wrap>
        <v-flex xs12 md12 sm12 lg12 pa-2>
            
      <v-card>
        <v-card-title primary-title>{{author.first_name  + '' + author.last_name}}</v-card-title>
        <v-card-text>{{author.bio}}</v-card-text>
      </v-card>
        </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      author: {
        id: null,
        first_name: null,
        last_name: null,
        description: null
      }
    };
  },
  methods: {
    getAuthor: function() {
      let endpoint = `api/books/author/${this.$route.params.id}/`;
      axios
        .get(endpoint)
        .then(res => {
          this.author = res.data;
        })
        .catch(err => {
          console.error(err);
        });
    },
    
  },
  mounted() {
    this.getAuthor();
  }
};
</script>