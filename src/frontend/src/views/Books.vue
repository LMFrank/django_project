<template>
  <v-container fluid>
    <v-btn color="primary" v-if="$user.get().role == 'staff'" @click="addBookDialog=true">
      Add Book &nbsp;
      <v-icon>mdi-book-plus</v-icon>
    </v-btn>

    <v-checkbox
      label="Read Books"
      v-model="my_books"
      value="value"
      v-if="$user.get().role == 'user' || $user.get().role == 'staff' "
      @change="getBooks"
    ></v-checkbox>
    <v-layout row wrap>
      <v-flex xs12 sm12 md6 lg4 v-for="(book, index) in books" :key="index" pa-2>
        <v-card class="mx-auto">
          <v-img
            v-if="book.cover"
            class="link-img white--text"
            height="600px"
            :src="book.cover"
            contain
            @click="$router.push({ path: `/books/${book.id}`})"
          ></v-img>
          <v-img
            v-else
            class="white--text link-img"
            height="600px"
            contain
            src="https://picsum.photos/288/434/"
            @click="$router.push({ path: `/books/${book.id}`})"
          ></v-img>
          <v-card-title primary-title>{{book.title}}</v-card-title>
          <v-card-text>
            <span class="text--primary">
              <span>{{book.description | truncate(120, '...')}}</span>
            </span>
          </v-card-text>

          <v-card-actions>
            <v-btn text color="orange" @click="$router.push({ path: `/books/${book.id}`})">Details</v-btn>
            <v-btn
              text
              color="info"
              v-if="$user.get().role=='staff'"
              @click="setEditedBook(index)"
            >Edit</v-btn>
            <v-btn
              text
              color="red"
              @click="setDeletedBook(book.id)"
              v-if="$user.get().role=='staff'"
            >Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>

    <!-- add Book dialog -->
    <v-dialog v-model="addBookDialog" max-width="600px" transition="dialog-transition">
      <v-card>
        <v-card-title primary-title>Add Book</v-card-title>
        <v-card-text>
          <v-layout row wrap>
            <!-- book title -->
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-text-field
                name="title"
                label="Book Title"
                v-model="newBook.title"
                prepend-icon="mdi-format-title"
              ></v-text-field>
            </v-flex>
            <!-- boook publication date -->
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-dialog
                ref="dialog"
                v-model="bookDateDialog"
                :return-value.sync="newBook.publication_date"
                persistent
                width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="newBook.publication_date"
                    label="Publication Date"
                    prepend-icon="mdi-calendar-today"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="newBook.publication_date" scrollable>
                  <div class="flex-grow-1"></div>
                  <v-btn text color="primary" @click="bookDateDialog = false">Cancel</v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="$refs.dialog.save(newBook.publication_date)"
                  >OK</v-btn>
                </v-date-picker>
              </v-dialog>
            </v-flex>
            <!-- book category -->
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-select
                :items="categories"
                v-model="newBook.category"
                label="Book Category"
                prepend-icon="mdi-format-list-bulleted-type"
                item-text="name"
                item-value="id"
                clearable
                required
              ></v-select>
            </v-flex>
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-file-input
                label="Book Cover"
                v-model="newBook.cover"
                prepend-icon="mdi-file-image"
                clearable
                accept="image/png, image/jpeg, image/bmp"
              ></v-file-input>
            </v-flex>
            <v-flex xs12 sm12 md12 lg12 pa-2>
              <v-select
                :items="authors"
                v-model="newBook.authors"
                label="Book Authors"
                prepend-icon="mdi-pen"
                :item-text="get_full_name"
                multiple
                chips
                item-value="id"
                clearable
                required
              ></v-select>
            </v-flex>
            <v-flex xs12 sm12 md12 lg12 pa-2>
              <v-textarea
                label="Book Description"
                name="description"
                prepend-icon="mdi-information-outline"
                v-model="newBook.description"
              ></v-textarea>
            </v-flex>
          </v-layout>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="addBookDialog=false">Cancel</v-btn>
            <v-btn color="success" @click="addBook">Add Book</v-btn>
          </v-card-actions>
        </v-card-text>
      </v-card>
    </v-dialog>
    <!-- end add Book dialog -->
    <!-- edit book dialog -->
    <v-dialog
      v-model="editBookDialog"
      max-width="600px"
      transition="dialog-transition"
      v-if="$user.get().role=='staff'"
    >
      <v-card>
        <v-card-title primary-title>Edit Book</v-card-title>
        <v-card-text>
          <v-layout row wrap>
            <!-- book title -->
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-text-field
                name="title"
                label="Book Title"
                v-model="editedBook.title"
                prepend-icon="mdi-format-title"
              ></v-text-field>
            </v-flex>
            <!-- boook publication date -->
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-dialog
                ref="editDialog"
                v-model="editBookDateDialog"
                :return-value.sync="editedBook.publication_date"
                persistent
                width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="editedBook.publication_date"
                    label="Publication Date"
                    prepend-icon="mdi-calendar-today"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="editedBook.publication_date" scrollable>
                  <div class="flex-grow-1"></div>
                  <v-btn text color="primary" @click="editBookDateDialog = false">Cancel</v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="$refs.editDialog.save(editedBook.publication_date)"
                  >OK</v-btn>
                </v-date-picker>
              </v-dialog>
            </v-flex>
            <!-- book category -->
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-select
                :items="categories"
                v-model="editedBook.category"
                label="Book Category"
                prepend-icon="mdi-format-list-bulleted-type"
                item-text="name"
                item-value="id"
                clearable
                required
              ></v-select>
            </v-flex>
            <v-flex xs12 sm12 md6 lg6 pa-2>
              <v-file-input
                label="Book Cover"
                v-model="editedBook.cover"
                prepend-icon="mdi-file-image"
                clearable
                accept="image/png, image/jpeg, image/bmp"
              ></v-file-input>
            </v-flex>
            <v-flex xs12 sm12 md12 lg12 pa-2>
              <v-select
                :items="authors"
                v-model="editedBook.authors"
                label="Book Authors"
                prepend-icon="mdi-pen"
                :item-text="get_full_name"
                multiple
                chips
                item-value="id"
                clearable
                required
              ></v-select>
            </v-flex>
            <v-flex xs12 sm12 md12 lg12 pa-2>
              <v-textarea
                label="Book Description"
                name="description"
                prepend-icon="mdi-information-outline"
                v-model="editedBook.description"
              ></v-textarea>
            </v-flex>
          </v-layout>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="editBookDialog=false">Cancel</v-btn>
            <v-btn color="success" @click="updateBook">Update</v-btn>
          </v-card-actions>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- delete book confirm dialog -->
    <v-dialog v-model="deleteBookDialog" max-width="400px" transition="dialog-transition">
      <v-card>
        <v-card-title primary-title>Delete Book ?</v-card-title>
        <v-card-text>
          This action will delete all reviews associated with this book!
          It will also delete it from users' libraries
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" text @click="deleteBook">I understand the risk</v-btn>
          <v-btn color="primary" text @click="deleteBookDialog=false">Take me back</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- end confirm delete dialog -->
  </v-container>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import cloneDeep from "clone-deep";
export default {
  data() {
    return {
      books: [],
      addBookDialog: false,
      bookDateDialog: false,
      editBookDialog: false,
      editBookDateDialog: false,
      deleteBookDialog: false,
      deletedBookId: null,
      newBook: {},
      editedBook: {},
      categories: [],
      authors: [],
      my_books: false
    };
  },
  methods: {
    getBooks: function() {
      let endpoint = "api/books/";
      if (this.my_books) {
        endpoint = "api/books/?mine=true";
      }
      axios
        .get(endpoint)
        .then(response => {
          this.books = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    getCategories: function() {
      let endpoint = "api/books/category/";
      axios
        .get(endpoint)
        .then(response => {
          this.categories = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    getAuthors: function() {
      let endpoint = "api/books/author/";
      axios
        .get(endpoint)
        .then(response => {
          this.authors = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    get_full_name: function(obj) {
      return obj.first_name + " " + obj.last_name;
    },

    addBook: function() {
      let endpoint = `api/books/`;
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
          "X-CSRFToken": csrf_token
        }
      };
      let bookFormData = new FormData();
      bookFormData.set("title", this.newBook.title);
      bookFormData.set("description", this.newBook.description);
      bookFormData.set("publication_date", this.newBook.publication_date);
      if (this.newBook.cover) bookFormData.set("cover", this.newBook.cover);
      bookFormData.set("category", this.newBook.category);
      bookFormData.set("authors", JSON.stringify(this.newBook.authors));

      axios
        .post(endpoint, bookFormData, config)
        .then(response => {
          this.$bvToast.toast("Book was added successfully", {
            title: `Book Add`,
            variant: "success",
            solid: true
          });
          this.getBooks();
          this.addBookDialog = false;
          this.newBook = {};
        })
        .catch(error => {
          console.log(error);
        })
        .finally(() => {});
    },
    setEditedBook: function(index) {
      this.editedBook.id = this.books[index].id;
      this.editedBook.cover = null;
      this.editedBook.category = this.books[index].category.id;
      this.editedBook.authors = [];
      for (let i = 0; i < this.books[index].authors.length; i++) {
        const element = this.books[index].authors[i];
        this.editedBook.authors.push(element.id);
      }
      this.editedBook.description = this.books[index].description;
      this.editedBook.title = this.books[index].title;

      this.editedBook.publication_date = this.books[index].publication_date;

      this.editBookDialog = true;
    },
    updateBook: function() {
      let endpoint = `api/books/${this.editedBook.id}/`;
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
          "X-CSRFToken": csrf_token
        }
      };
      let bookFormData = new FormData();
      bookFormData.set("title", this.editedBook.title);
      bookFormData.set("description", this.editedBook.description);
      bookFormData.set("publication_date", this.editedBook.publication_date);
      if (this.editedBook.cover)
        bookFormData.set("cover", this.editedBook.cover);
      bookFormData.set("category", this.editedBook.category);
      bookFormData.set("authors", JSON.stringify(this.editedBook.authors));

      axios
        .patch(endpoint, bookFormData, config)
        .then(response => {
          this.$bvToast.toast("Book was updated successfully", {
            title: `Book Update`,
            variant: "success",
            solid: true
          });
          this.getBooks();
          this.edited = false;
          this.editedBook = {};
          this.editBookDialog = false;
        })
        .catch(error => {
          console.log(error);
        })
        .finally(() => {});
    },
    setDeletedBook: function(id) {
      this.deleteBookDialog = true;
      this.deletedBookId = id;
    },
    deleteBook: function() {
      let endpoint = `api/books/${this.deletedBookId}/`;
      let csrf_token = Cookies.get("csrftoken");
      let config = {
        headers: {
          "X-CSRFToken": csrf_token
        }
      };
      axios
        .delete(endpoint, config)
        .then(res => {
          this.$bvToast.toast("Book was deleted successfully", {
            title: `Book Delete`,
            variant: "success",
            solid: true
          });
          this.deleteBookDialog = false;
          this.deletedBookId = null;
          this.getBooks();
        })
        .catch(err => {
          console.error(err);
        });
    }
  },
  mounted() {
    this.getBooks();
    this.getCategories();
    this.getAuthors();
  }
};
</script>

<style scoped>
.link-img {
  cursor: pointer;
}
</style>