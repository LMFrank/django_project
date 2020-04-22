<template>
  <v-container>
    <v-btn color="primary" @click="addDialog=true" v-if="$user.get().role=='staff'">
      Add Author
      &nbsp;
      <v-icon>mdi-pen</v-icon>
    </v-btn>
    <v-layout row wrap>
      <v-flex xs12 md12 sm12 lg12 pa-5>
        <v-expansion-panels>
          <v-expansion-panel v-for="(author,i) in authors" :key="i">
            <v-expansion-panel-header>
              <h3>{{author.first_name + ' ' + author.last_name}}</h3>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card>
                <v-card-text>{{author.bio | truncate(120, '...')}}</v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="success"
                    text
                    @click="$router.push({ path: `/author/${author.id}`})"
                  >Details</v-btn>
                  <v-btn
                    color="error"
                    text
                    @click="setDeletedItem(author.id)"
                    v-if="$user.get().role=='staff'"
                  >Delete</v-btn>
                  <v-btn
                    color="info"
                    @click="setEditedItem(i)"
                    text
                    v-if="$user.get().role=='staff'"
                  >Edit</v-btn>
                </v-card-actions>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-flex>
    </v-layout>
    <!-- delete dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px" transition="dialog-transition">
      <v-card>
        <v-card-title primary-title>Delete Author ?</v-card-title>
        <v-card-text>This action will delete this author, it will also delete his/her association with all of his/her books</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" text @click="deleteItem">I understand the risk</v-btn>
          <v-btn color="primary" text @click="deleteDialog=false">Take me back</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- end delete dialog -->

    <!-- start add dialog -->
    <v-dialog
      v-model="addDialog"
      max-width="500px"
      transition="dialog-transition"
      v-if="$user.get().role=='staff'"
    >
      <v-card>
        <v-card-title>Add Author</v-card-title>
        <v-card-text>
          <v-layout row wrap>
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-text-field name="name" label="First Name" v-model="newAuthor.first_name"></v-text-field>
            </v-flex>
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-text-field name="name" label="Last Name" v-model="newAuthor.last_name"></v-text-field>
            </v-flex>
            <v-flex xs12 sm12 md12 pa-2>
              <v-textarea name="bio" label="Bio" v-model="newAuthor.bio"></v-textarea>
            </v-flex>
          </v-layout>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="addDialog=false">Cancel</v-btn>
          <v-btn color="success" @click="addAuthor">Add Author</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- end add dialog -->

    <!-- start edit dialog -->
    <v-dialog
      v-model="editDialog"
      max-width="500px"
      transition="dialog-transition"
      v-if="$user.get().role=='staff'"
    >
      <v-card>
        <v-card-title>Edit Author</v-card-title>
        <v-card-text>
          <v-layout row wrap>
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-text-field name="name" label="First Name" v-model="editedItem.first_name"></v-text-field>
            </v-flex>
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-text-field name="name" label="Last Name" v-model="editedItem.last_name"></v-text-field>
            </v-flex>

            <v-flex xs12 sm12 md12 pa-2>
              <v-textarea name="bio" label="Bio" v-model="editedItem.bio"></v-textarea>
            </v-flex>
          </v-layout>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="editDialog=false">Cancel</v-btn>
          <v-btn color="success" @click="editItem">Update</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- end edit dialog -->
  </v-container>
</template>


<script>
import axios from "axios";
import Cookies from "js-cookie";

export default {
  data() {
    return {
      authors: [],
      newAuthor: {},
      addDialog: false,
      deleteDialog: false,
      deletedItem: null,
      editedItem: {},
      editDialog: false,
      deleteDialog: false,
      newAuthor: {}
    };
  },
  methods: {
    getAuthors: function() {
      let endpoint = "api/books/author/";
      axios
        .get(endpoint)
        .then(res => {
          this.authors = res.data;
        })
        .catch(err => {
          console.error(err);
        });
    },
    setDeletedItem: function(id) {
      this.deletedItem = id;
      this.deleteDialog = true;
    },
    setEditedItem: function(index) {
      this.editedItem.id = this.authors[index].id;
      this.editedItem.first_name = this.authors[index].first_name;
      this.editedItem.last_name = this.authors[index].last_name;

      this.editedItem.bio = this.authors[index].bio;
      this.editDialog = true;
    },
    deleteItem: function() {
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };
      let endpoint = `api/books/author/${this.deletedItem}/`;
      axios
        .delete(endpoint, config)
        .then(res => {
          this.$bvToast.toast("Author was deleted successfully", {
            title: `Author Delete`,
            variant: "success",
            solid: true
          });
          this.getAuthors();
          this.deleteDialog = false;
        })
        .catch(err => {
          console.error(err);
        });
    },
    addAuthor: function() {
      let endpoint = "api/books/author/";
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };

      axios
        .post(endpoint, this.newAuthor, config)
        .then(res => {
          this.$bvToast.toast("Author was added successfully", {
            title: `Author Add`,
            variant: "success",
            solid: true
          });
          this.getAuthors();
          this.newAuthor = {};
          this.addDialog = false;
        })
        .catch(err => {
          console.error(err);
        });
    },
    editItem: function() {
      let endpoint = `api/books/author/${this.editedItem.id}/`;
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };

      axios
        .patch(endpoint, this.editedItem, config)
        .then(res => {
          this.$bvToast.toast("Author was updated successfully", {
            title: `Author Update`,
            variant: "success",
            solid: true
          });
          this.getAuthors();
          this.editedItem = {};
          this.editDialog = false;
        })
        .catch(err => {
          console.error(err);
        });
    }
  },
  mounted() {
    this.getAuthors();
  }
};
</script>
