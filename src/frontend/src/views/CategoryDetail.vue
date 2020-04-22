<template>
  <v-container>
    <v-layout row wrap>
        <v-flex xs12 md12 sm12 lg12 pa-2>
            
      <v-card>
        <v-card-title primary-title>{{category.name}}</v-card-title>
        <v-card-text>{{category.description}}</v-card-text>
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
      category: {
        id: null,
        name: null,
        description: null
      }
    };
  },
  methods: {
    getCategory: function() {
      let endpoint = `api/books/category/${this.$route.params.id}/`;
      axios
        .get(endpoint)
        .then(res => {
          this.category = res.data;
        })
        .catch(err => {
          console.error(err);
        });
    },
    
  },
  mounted() {
    this.getCategory();
  }
};
</script>