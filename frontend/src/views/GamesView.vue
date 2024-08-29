<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <!-- bootswatch cdn sketchy -->
      <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/sketchy/bootstrap.min.css"
        integrity="sha384-RxqHG2ilm4r6aFRpGmBbGTjsqwfqHOKy1ArsMhHusnRO47jcGqpIQqlQK/kmGy9R"
        crossorigin="anonymous"
      />
      <div class="row">
        <div class="col-sm 12">
          <h1
            class="text-center bg-primary text-white"
            style="border-radius: 10px"
          >
            Games Library 🕹️
          </h1>
          <hr />
          <br />

          <!-- Alert message -->
          <b-alert v-model="showMessage" variant="success" show>
            {{ message }}
          </b-alert>
          <button class="btn btn-success btn-sm" v-b-modal.game-modal>
            Add Game
          </button>
          <br /><br />

          <table class="table table-hover">
            <!-- Table Header -->
            <thead>
              <tr>
                <!-- Table header cells -->
                <th scope="col">Title</th>
                <th scope="col">Genre</th>
                <th scope="col">Played?</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(game, index) in games" :key="index">
                <!-- Table header cells -->
                <td>{{ game.title }}</td>
                <td>{{ game.genre }}</td>
                <td>{{ game.played ? "Yes" : "No" }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button
                      class="btn btn-info btn-sm"
                      @click="editGame(game)"
                      v-b-modal.game-update-modal
                    >
                      Update
                    </button>
                    <button
                      class="btn btn-danger btn-sm"
                      @click="deleteGame(game.id)"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <footer
            class="bg-primary text-white text-center"
            style="border-radius: 10px"
          >
            Copyrights &copy;. All Rights Reserved 2024
          </footer>
        </div>
      </div>

      <!-- Start of add game modal -->
      <b-modal
        ref="addGameModal"
        id="game-modal"
        title="Add a new game"
        hide-footer
      >
        <b-form @submit="onSubmit" @reset="onReset" class="w100">
          <!-- form goup for title entry -->
          <b-form-group
            id="form-title-group"
            class="mb-4"
            label="Title:"
            label-for="form-title-input"
            floating
          >
            <!-- form goup for title entry -->
            <b-form-input
              id="form-title-input"
              type="text"
              v-model="addGameForm.title"
              required
              placeholder="Enter Game"
            >
            </b-form-input>
          </b-form-group>

          <!-- form goup for genre entry -->
          <b-form-group
            id="form-title-group"
            class="mb-4"
            label="Genre:"
            label-for="form-title-input"
            floating
          >
            <b-form-input
              id="form-genre-input"
              type="text"
              v-model="addGameForm.genre"
              required
              placeholder="Enter Genre"
            >
            </b-form-input>
          </b-form-group>

          <!-- Checkbox -->
          <b-form-group id="form-played-group" class="mb-4 pl-4">
            <input
              id="form-checkbox"
              v-model="addGameForm.played"
              type="checkbox"
            />
            <label for="form-checkbox"> Played? </label>
          </b-form-group>

          <!-- buttons: Submit & Reset -->
          <b-button type="submit" variant="outline-info">Submit</b-button>
          <b-button type="reset" variant="outline-danger">Reset</b-button>
        </b-form>
      </b-modal>
      <!-- End of add game modal -->

      <!-- Start of update game modal -->
      <b-modal
        ref="editGameModal"
        id="game-update-modal"
        title="Update the game"
        hide-footer
      >
        <b-form @submit="onSubmitUpdate" @reset="onCancelUpdate" class="w100">
          <b-form-group
            id="form-title-edit-group"
            class="mb-4"
            label="Title:"
            label-for="form-title-edit-input"
            floating
          >
            <!-- form goup for title entry -->
            <b-form-input
              id="form-title-edit-input"
              type="text"
              v-model="editGameForm.title"
              required
              placeholder="Enter Game"
            >
            </b-form-input>
          </b-form-group>

          <!-- form goup for genre entry -->
          <b-form-group
            id="form-title-edit-group"
            class="mb-4"
            label="Genre:"
            label-for="form-title-edit-input"
            floating
          >
            <b-form-input
              id="form-title-edit-genre"
              type="text"
              v-model="editGameForm.genre"
              required
              placeholder="Enter Genre"
            >
            </b-form-input>
          </b-form-group>

          <!-- Checkbox -->
          <b-form-group id="form-played-edit-group" class="mb-4 pl-4">
            <input
              id="form-edit-checkbox"
              v-model="editGameForm.played"
              type="checkbox"
            />
            <label for="form-edit-checkbox"> Played? </label>
          </b-form-group>

          <!-- buttons: Submit & Reset -->
          <b-button type="submit" variant="outline-info">Update</b-button>
          <b-button type="reset" variant="outline-danger">Cancel</b-button>
        </b-form>
      </b-modal>
      <!-- End of update game modal -->
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const games = ref([]);
const addGameForm = ref({
  title: "",
  genre: "",
  played: false,
});
const editGameForm = ref({
  title: "",
  genre: "",
  played: false,
});

// $refs to modal
const addGameModal = ref(null);
const editGameModal = ref(null);

const message = ref("");
const showMessage = ref(false);

// GET function
const getGames = () => {
  const path = "http://localhost:5000/games";

  axios
    .get(path)
    .then((res) => (games.value = res.data.games))
    .catch((err) => console.log(err));
};

// POST function
const addGame = (payload) => {
  const path = "http://localhost:5000/games";

  axios
    .post(path, payload)
    .then(() => {
      getGames();
      message.value = "Game Added!";
      showMessage.value = true;
      setTimeout(() => {
        showMessage.value = false;
      }, 3000);
    })
    .catch((err) => {
      console.log(err);
      getGames();
    });
};

// PUT function
const updateGame = (payload, gameID) => {
  const path = `http://localhost:5000/games/${gameID}`;

  axios
    .put(path, payload)
    .then(() => {
      getGames();
      message.value = "Game Updated!";
      showMessage.value = true;
      setTimeout(() => {
        showMessage.value = false;
      }, 3000);
    })
    .catch((err) => {
      console.log(err);
      getGames();
    });
};

const deleteGame = (gameID) => {
  const path = `http://localhost:5000/games/${gameID}`;

  axios
    .delete(path)
    .then(() => {
      getGames();
      message.value = "Game Deleted!";
      showMessage.value = true;
      setTimeout(() => {
        showMessage.value = false;
      }, 3000);
    })
    .catch((err) => {
      console.log(err);
      getGames();
    });
};

const onSubmit = (e) => {
  e.preventDefault();
  addGameModal.value.hide();

  const payload = {
    title: addGameForm.value.title,
    genre: addGameForm.value.genre,
    played: addGameForm.value.played ? true : false,
  };

  addGame(payload);
  initForm();
};

const onSubmitUpdate = (e) => {
  e.preventDefault();
  editGameModal.value.hide();

  const payload = {
    title: editGameForm.value.title,
    genre: editGameForm.value.genre,
    played: editGameForm.value.played ? true : false,
  };

  updateGame(payload, editGameForm.value.id);
  initForm();
};

const onReset = (e) => {
  e.preventDefault();
  addGameModal.value.hide();

  initForm();
};

const onCancelUpdate = (e) => {
  e.preventDefault();
  editGameModal.value.hide();

  initForm();
  getGames();
};

const editGame = (game) => {
  editGameForm.value = game;
};

const initForm = () => {
  addGameForm.value.title = "";
  addGameForm.value.genre = "";
  addGameForm.value.played = false;
  editGameForm.value.id = "";
  editGameForm.value.title = "";
  editGameForm.value.genre = "";
  editGameForm.value.played = false;
};

onMounted(() => {
  getGames();
});
</script>

<style scoped>
label[for="form-checkbox"],
label[for="form-edit-checkbox"] {
  cursor: pointer;
}
</style>
