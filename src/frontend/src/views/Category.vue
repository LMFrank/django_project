<template>
  <v-container>
    <v-btn color="primary" @click="addDialog=true" v-if="$user.get().role=='staff'">
      Add Category
      &nbsp;
      <v-icon>mdi-playlist-plus</v-icon>
    </v-btn>
    <v-layout row wrap>
      <v-flex xs12 md12 sm12 lg12 pa-5>
        <v-expansion-panels>
          <v-expansion-panel v-for="(category,i) in categories" :key="i">
            <v-expansion-panel-header>
              <h3>{{category.name}}</h3>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card>
                <v-card-text>{{category.description | truncate(120, '...')}}</v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="success"
                    text
                    @click="$router.push({ path: `/category/${category.id}`})"
                  >Details</v-btn>
                  <v-btn
                    color="error"
                    text
                    @click="setDeletedItem(category.id)"
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
        <v-card-title primary-title>Delete Category ?</v-card-title>
        <v-card-text>
          This action will delete this category and all books associated with it !
          Not only that, It will also delete all reviews associated with those books
        </v-card-text>
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
        <v-card-title>Add Category</v-card-title>
        <v-card-text>
          <v-layout row wrap>
            <v-flex xs12 sm12 md12 pa-2>
              <v-text-field name="name" label="Category Name" v-model="newCategory.name"></v-text-field>
            </v-flex>

            <v-flex xs12 sm12 md12 pa-2>
              <v-textarea
                name="description"
                label="Category Description"
                v-model="newCategory.description"
              ></v-textarea>
            </v-flex>
          </v-layout>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="addDialog=false">Cancel</v-btn>
          <v-btn color="success" @click="addCategory">Add Category</v-btn>
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
        <v-card-title>Edit Category</v-card-title>
        <v-card-text>
          <v-layout row wrap>
            <v-flex xs12 sm12 md12 pa-2>
              <v-text-field name="name" label="Category Name" v-model="editedItem.name"></v-text-field>
            </v-flex>

            <v-flex xs12 sm12 md12 pa-2>
              <v-textarea
                name="description"
                label="Category Description"
                v-model="editedItem.description"
              ></v-textarea>
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
      categories: [],
      newCategory: {},
      addDialog: false,
      deleteDialog: false,
      deletedItem: null,
      editedItem: {},
      editDialog: false,
      deleteDialog: false,
      newCategory: {}
    };
  },
  methods: {
    getCategories: function() {
      let endpoint = "api/books/category/";
      axios
        .get(endpoint)
        .then(res => {
          this.categories = res.data;
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
      this.editedItem.id = this.categories[index].id;
      this.editedItem.name = this.categories[index].name;
      this.editedItem.description = this.categories[index].description;
      this.editDialog = true;
    },
    deleteItem: function() {
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };
      let endpoint = `api/books/category/${this.deletedItem}/`;
      axios
        .delete(endpoint, config)
        .then(res => {
          this.$bvToast.toast("Category was deleted successfully", {
            title: `Category Delete`,
            variant: "success",
            solid: true
          });
          this.getCategories();
          this.deleteDialog = false;
        })
        .catch(err => {
          console.error(err);
        });
    },
    addCategory: function() {
      let endpoint = "api/books/category/";
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };

      axios
        .post(endpoint, this.newCategory, config)
        .then(res => {
          this.$bvToast.toast("Category was added successfully", {
            title: `Category Add`,
            variant: "success",
            solid: true
          });
          this.getCategories();
          this.newCategory = {};
          this.addDialog = false;
        })
        .catch(err => {
          console.error(err);
        });
    },
    editItem: function() {
      let endpoint = `api/books/category/${this.editedItem.id}/`;
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };

      axios
        .patch(endpoint, this.editedItem, config)
        .then(res => {
          this.$bvToast.toast("Category was updated successfully", {
            title: `Category Update`,
            variant: "success",
            solid: true
          });
          this.getCategories();
          this.editedItem = {};
          this.editDialog = false;
        })
        .catch(err => {
          console.error(err);
        });
    }
  },
  mounted() {
    this.getCategories();
  }
};
</script>
