<template>
  <nav class="nav d-flex align-items-center justify-content-between">
    <div class="auto-suggest search-input">
      <vs-input v-model="query" placeholder="Search..." class="" />
      <div class="suggest-list" v-if="suggestList.length > 0">
        <p
          class="pointer"
          v-for="suggest in suggestList"
          :key="suggest.id"
          @click="selectSuggest(suggest)"
        >
          {{ suggest.location }}
        </p>
      </div>

      <div class="suggest-list" v-if="isNoResult && query !== ''">
        <p>No cameras found!</p>
      </div>
    </div>

    <div class="d-flex justify-content-end align-items-end" style="width: 30%">
      <vs-button icon flat class="add-btn mr-2" @click="active = !active">
        <i class="bx bx-filter-alt"></i>
      </vs-button>
      <vs-button icon flat class="add-btn" @click="addNewCamera">
        <i class="bx bx-plus"> </i>
      </vs-button>
    </div>

    <!-- dialog -->
    <vs-dialog not-close v-model="active">
      <div class="con-form">
        <div class="row">
          <div class="col-12">
            <p class="m-0">Filtering by type</p>
            <div class="divider"></div>
          </div>

          <div class="col-12 mb-4 d-flex">
            <vs-checkbox v-model="localFilter.type" val="Dome">
              Dome
            </vs-checkbox>
            <vs-checkbox v-model="localFilter.type" val="Bullet">
              Bullet
            </vs-checkbox>
          </div>
          <div class="col-12">
            <p class="m-0">Filtering by status</p>
            <div class="divider"></div>
          </div>
          <div class="col-12 d-flex">
            <vs-checkbox v-model="localFilter.status" val="Good">
              Good
            </vs-checkbox>
            <vs-checkbox v-model="localFilter.status" val="Disabled">
              Disabled
            </vs-checkbox>
          </div>

          <div class="col-12 mt-3 mb-1">
            <vs-button
              size="large"
              @click="confirmFilter"
              class="w-100 add-btn"
            >
              Done
            </vs-button>
          </div>
        </div>
      </div>
    </vs-dialog>

    <vue-bottom-sheet
      overlay
      click-to-close
      rounded
      max-height="100%"
      ref="newCamera"
      @closed="active2 = false"
    >
      <div class="model-body">
        <AddNewCamera
          @completed="closeModal"
          @closeModal="closeModal"
          v-if="active2"
        />
      </div>
    </vue-bottom-sheet>
  </nav>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";
import AddNewCamera from "./AddNewCamera.vue";
import VueBottomSheet from "@webzlodimir/vue-bottom-sheet";

export default {
  data() {
    return {
      query: "",
      active: false,
      suggestList: [],
      isSelected: false,
      isNoResult: false,
      localFilter: {
        type: ["Dome", "Bullet"],
        status: ["Good", "Disabled"],
      },
      active2: false,
    };
  },
  components: {
    VueBottomSheet,
    AddNewCamera,
  },
  watch: {
    query(value) {
      this.getCameras(value);
      this.isSelected = false;
    },
  },
  computed: {
    ...mapState(["filter"]),
  },
  created() {
    this.localFilter = this.filter;
  },
  methods: {
    closeModal() {
      this.$refs.newCamera.close();
      this.active2 = false;
    },
    addNewCamera() {
      this.$refs.newCamera.open();
      this.active2 = true;
    },
    confirmFilter() {
      this.active = false;
      this.$store.commit("setFilter", this.localFilter);
      this.$store.dispatch("getCameras");
    },
    getCameras(location) {
      if (!this.isSelected) {
        var status = "";
        var type = "";
        if (this.filter.status.length !== 2) {
          status = this.filter.status[0];
        }
        if (this.filter.type.length !== 2) {
          type = this.filter.type[0];
        }
        const queries = `?location=${location}&status=${status}&type=${type}`;

        axios
          .get("api/getCameras/" + queries)
          .then((res) => {
            if (res.data.length == 0) {
              this.isNoResult = true;
            } else {
              this.isNoResult = false;
            }
            this.suggestList = res.data;
          })
          .catch((err) => {
            this.$noti.display(err, "", "error", "danger");
          });
      }
    },
    selectSuggest(selectedValue) {
      this.query = selectedValue.location;
      this.suggestList = [];
      this.isSelected = true;
      this.$store.commit("setCenter", [
        selectedValue.latitude,
        selectedValue.longitude,
      ]);
    },
  },
};
</script>

<style >
.search-input {
  width: 70%;
}
.suggest-list {
  max-height: 50vh;
  overflow-y: scroll;
  position: absolute;
  width: 84%;
  z-index: 10000;
  background: #fff;
  border-radius: 12px;
  padding: 10px;
  margin-top: 10px;
  box-shadow: 0px 4px 25px -8px rgb(0 0 0 / 20%);
}
.suggest-list p {
  margin: 0px;
  padding: 5px;
  background: rgb(var(--vs-primary), 0.2);
  margin-bottom: 5px;
  border-radius: 5px;
}
.suggest-list p:hover {
  color: rgb(var(--vs-primary));
}
.nav {
  height: 60px;
  padding: 0px 15px;
  background: rgb(var(--vs-background-2));
  box-shadow: 0px 4px 25px -8px rgb(var(--vs-dark), 0.2);
}
</style>