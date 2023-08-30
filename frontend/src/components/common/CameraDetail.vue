<template>
  <div class="row">
    <div class="col-12 form-body" v-if="!openForm">
      <div class="row">
        <div class="col-12 mb-2">
          <div class="images">
            <img
              class
              v-for="(src, imageIndex) in images"
              :key="imageIndex"
              @click="index = imageIndex"
              v-lazy="src"
            />
          </div>
        </div>

        <div class="col-12">
          <p>
            <span class="font-weight-bold">Location</span> :
            {{ camera.location }}
          </p>
          <p>
            <span class="font-weight-bold">Latitude</span> :
            {{ camera.latitude }}
          </p>
          <p>
            <span class="font-weight-bold">Longitude</span> :
            {{ camera.longitude }}
          </p>
          <p>
            <span class="font-weight-bold">Status</span> : {{ camera.status }}
          </p>
          <p><span class="font-weight-bold">Type</span> : {{ camera.type }}</p>
        </div>
        <div class="col-12 px-0">
          <div class="divider"></div>
        </div>

        <div class="col-12" style="margin-bottom: 80px">
          <p class="font-weight-bold">Activities</p>

          <div
            v-for="(activity, index) in camera.activities"
            class="activity"
            :key="index"
          >
            <p
              :class="
                activity.cameraStatus == 'Good' ? 'success-span' : 'danger-span'
              "
            >
              Someone has updated status to
              "{{ activity.cameraStatus }}"
              at
              {{ $moment(activity.created_at).format("MM/DD/YYYY hh:mm a") }}!
            </p>
            <img
              v-lazy="apiUrl+activity.image"
              v-if="activity.image"
              class="w-100 "
              style="border-radius: 10px; margin-bottom: 10px"
              alt=""
            />
            <p class="mb-0">{{ activity.note }}</p>
          </div>
        </div>

        <div class="col-12 bottom-btn">
          <vs-button class="w-100" size="large" @click="openForm = !openForm">
            Update camera details
          </vs-button>
        </div>
      </div>
    </div>

    <div class="col-12" v-if="openForm">
      <div class="update-form">
        <UpdateCamera
          :camera="camera"
          @completed="completedUpdateCamera"
          @cancel="openForm = !openForm"
        />
      </div>
    </div>

    <CoolLightBox
      :items="images"
      :useZoomBar="true"
      :index="index"
      @close="index = null"
    >
    </CoolLightBox>
  </div>
</template>

<script>
import CoolLightBox from "vue-cool-lightbox";
import "vue-cool-lightbox/dist/vue-cool-lightbox.min.css";
import {API_URL} from '../../assets/constants/data'
import UpdateCamera from "./UpdateCamera";
export default {
  props: {
    camera: {},
  },
  data() {
    return {
      visible: false,
      apiUrl:API_URL,
      index: null,
      images: [],
      isReady: false,
      openForm: false,
      url: "http://mt0.google.com/vt/hl=en&x={x}&y={y}&z={z}&s={s}",
    };
  },
  components: {
    CoolLightBox,
    UpdateCamera,
  },
  created() {},
  mounted() {
    this.setImages();
  },
  watch: {},
  methods: {
    completedUpdateCamera(activity) {
      this.camera.status = activity.cameraStatus;
      this.camera.activities = [activity, ...this.camera.activities];
      this.openForm = false;
    },
    setImages() {
      var data = [];
      this.camera.images.forEach((image) => {
        data.push(this.apiUrl+image.image);
      });
      this.images = data;
      this.camera.activities = this.camera.activities.reverse();
    },
    showImg(index) {
      this.index = index;
      this.visible = true;
    },
    handleHide() {
      this.visible = false;
    },
  },
};
</script>

<style scoped>
.activity {
  background: rgba(0, 0, 0, 0.05);
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 15px;
}
.update-btn button {
  width: 100%;
  height: 150px;
  border-radius: 12px;
  border: 3px dashed rgb(var(--vs-primary));
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(var(--vs-primary), 0.2);
  flex-direction: column;
  color: rgb(var(--vs-primary));
  box-shadow: 0px 4px 25px -8px rgba(var(--vs-primary), 0.5);
  margin-bottom: 20px;
}
.update-btn button i {
  font-size: 35px;
}

.images img {
  width: 100%;
  max-width: calc(100vw - 30px);
  height: 150px;
  object-fit: cover;
  margin-right: 3px;
}
.nav {
  height: 60px;
  padding: 0px 15px;
  background: rgb(var(--vs-background-2));
  box-shadow: 0px 4px 25px -8px rgb(var(--vs-dark), 0.2);
  position: fixed;
  top: 0;
  right: 0;
  left: 0px;
  z-index: 99998;
}
.form-body {
  padding-top: 10px;
}
.images {
  display: flex;
  overflow-y: auto;
  border-radius: 12px;
}
</style>