<template>
  <v-container ma-auto>
    <v-layout row wrap justify-center>
      <v-flex xs10 sm10 md10 lg10>
        <v-card>
          <v-img v-if="book.cover" contain height="800" :src="book.cover"></v-img>
          <v-img v-else height="800" contain src="https://picsum.photos/288/434/"></v-img>
          <v-card-title primary-title>
            <h2>{{book.title}}</h2>
          </v-card-title>
          <v-card-title>
            <h3 style="color:orange">Category : {{book.category.name}}</h3>
            <v-spacer></v-spacer>
            <div v-if="$user.get().role !=='guest'">
              <v-btn color="warning" text v-if="book_read" @click="toggle_read">
                <v-icon>mdi-read</v-icon>Mark Unread
              </v-btn>
              <v-btn color="success" text v-else @click="toggle_read">
                <v-icon>mdi-check</v-icon>Mark Read
              </v-btn>
            </div>
          </v-card-title>
          <br />
          <v-card-text>{{book.description}}</v-card-text>
          <v-card-title primary-title>Reviews : {{reviews_count}}</v-card-title>
          <v-card-text>
            <v-layout row wrap justify-center>
              <v-flex xs8 sm8 md8 lg8>
                <div v-if="my_review.id">
                  <v-textarea
                    label="Update review"
                    v-model="my_review.text"
                    prepend-icon="mdi-comment"
                  ></v-textarea>
                  <v-btn color="success" text @click="updateReview">Update</v-btn>
                  <v-btn color="error" text @click="deleteReview">Delete</v-btn>
                </div>
                <div v-else>
                  <div v-if="$user.get().role !== 'guest'">
                    <v-textarea label="Add review" v-model="new_review.text"></v-textarea>
                    <v-btn color="success" text @click="addReview">Add Review</v-btn>
                  </div>
                </div>
                <br />
                <br />

                <v-list-item two-line v-for="(review, index) in reviews" :key="index">
                  <v-list-item-content>
                    <v-list-item-title>{{review.text}}</v-list-item-title>
                    <v-list-item-subtitle>
                      {{review.timestamp | moment("from", "now")}} by
                      <i>{{review.user}}</i>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
export default {
  data() {
    return {
      book: {
        category: {
          name: ""
        },
        cover: null
      },
      my_review: {},
      new_review: {},
      reviews: [],
      reviews_count: 0,
      disable_review: true,
      book_read: false
    };
  },
  methods: {
    getCurrentBook: function() {
      let endpoint = `api/books/${this.$route.params.id}/`;
      axios
        .get(endpoint)
        .then(res => {
          this.book = res.data;
        })
        .catch(err => {
          console.error(err);
        });
    },
    getBookReviews: function() {
      let endpoint = `api/books/${this.$route.params.id}/reviews/`;
      axios
        .get(endpoint)
        .then(res => {
          this.reviews_count = res.data.length;
          for (let index = 0; index < res.data.length; index++) {
            if (res.data[index].user.id === this.$user.get().id) {
              this.my_review = {
                id: res.data[index].id,
                text: res.data[index].text
              };
            } else {
              this.reviews.push({
                id: res.data[index].id,
                text: res.data[index].text,
                timestamp: res.data[index].timestamp,
                user: res.data[index].user.username
              });
            }
          }
        })
        .catch(err => {
          console.error(err);
        });
    },
    addReview: function() {
      let endpoint = `api/books/${this.$route.params.id}/reviews/`;
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };
      axios
        .post(endpoint, this.new_review, config)
        .then(res => {
          this.new_review = {};
          this.$bvToast.toast("Review was added successfully", {
            title: `Review Added`,
            variant: "success",
            solid: true
          });
          this.getBookReviews();
        })
        .catch(err => {
          console.error(err);
        });
    },
    updateReview: function() {
      let endpoint = `api/reviews/${this.my_review.id}/`;
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };
      axios
        .patch(endpoint, this.my_review, config)
        .then(res => {
          this.$bvToast.toast("Review was udapted successfully", {
            title: `Review Update`,
            variant: "success",
            solid: true
          });
          this.getBookReviews();
        })
        .catch(err => {
          console.error(err);
        });
    },
    deleteReview: function() {
      let endpoint = `api/reviews/${this.my_review.id}/`;
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };
      axios
        .delete(endpoint, config)
        .then(res => {
          this.my_review = {};
          this.getBookReviews();
          this.$bvToast.toast("Review was deleted successfully", {
            title: `Review Delete`,
            variant: "success",
            solid: true
          });
        })
        .catch(err => {
          console.error(err);
        });
    },
    getReadStatus: function() {
      if (this.$user.get().role !== "guest") {
        let endpoint = `api/books/${this.$route.params.id}/read/`;
        axios
          .get(endpoint)
          .then(res => {
            this.book_read = res.data.read;
          })
          .catch(err => {
            console.error(err);
          });
      }
    },
    toggle_read: function() {
      let endpoint = `api/books/${this.$route.params.id}/read/`;
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };
      axios
        .post(endpoint, {}, config)
        .then(res => {
          this.getReadStatus();
        })
        .catch(err => {
          console.error(err);
        });
    }
  },
  mounted() {
    this.getCurrentBook();
    this.getBookReviews();
    this.getReadStatus();
  }
};
</script>