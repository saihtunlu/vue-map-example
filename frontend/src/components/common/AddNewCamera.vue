<template>
  <div class="row">
    <div class="col-12 form-body">
      <div class="row">
        <div class="col-12">
          <label style="font-size: 0.75rem; padding-left: 10px" class="mb-0">Media</label>
        </div>

        <div class="col-12">
          <div class="row mx-0 media-box">
            <div
              class="col-4 px-0 mb-2 selected-images"
              v-for="(image, index) in selectedImages"
              :key="image.url"
            >
              <span class="remove-image" @click="removeImage(index)"
                ><i class="bx bx-x"></i
              ></span>
              <img :src="image.url" alt="" />
            </div>
            <div class="col-4 pointer mb-2 px-0">
              <input
                type="file"
                ref="fileInput"
                multiple
                hidden
                class="uploader pointer"
                @change="onFileChange"
                name=""
              />
              <div class="file-uploader" @click="$refs.fileInput.click()">
                <i class="bx bx-camera"></i>
                <p>Add Images</p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-12">
          <label class="custom-label mb-0">Location (auto generate)</label>
          <textarea
            class="custom-textarea"
            v-model="camera.location"
          ></textarea>
        </div>
        <div class="col-6 pr-2">
          <vs-input
            label="Latitude  (auto generate)"
            v-model="camera.latitude"
          />
        </div>
        <div class="col-6 pl-2">
          <vs-input
            label="Longitude (auto generate)"
            v-model="camera.longitude"
          />
        </div>
        <div class="col-12 mt-3">
          <CenterGetter :center="center" @getCenter="getCenter" />
        </div>
        <div class="col-12">
          <vs-select label="Camera Type" v-model="camera.type">
            <vs-option label="Dome" value="Dome"> Dome </vs-option>
            <vs-option label="Bullet" value="Bullet"> Bullet </vs-option>
          </vs-select>
        </div>
        <div class="col-12" style="margin-bottom: 80px">
          <vs-select label="Camera Status" v-model="camera.status">
            <vs-option label="Good" value="Good"> Good </vs-option>
            <vs-option label="Disabled" value="Disabled"> Disabled </vs-option>
          </vs-select>
        </div>
        <div class="col-12 bottom-btn">
          <vs-button
            class="w-100"
            size="large"
            :loading="isLoading"
            @click="Post"
            >Save
          </vs-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CenterGetter from "../common/CenterGetter";
import axios from "axios";
import { mapState } from "vuex";
export default {
  data() {
    return {
      selectedImages: [],
      camera: {
        location: "",
        status: "Good",
        type: "Dome",
        latitude: "",
        longitude: "",
      },
      isLoading: false,
      center: [16.819814400000002, 96.1511424], //yangon
    };
  },
  components: {
    CenterGetter,
  },
  mounted() {
    if (this.currentLocation.length !== 0) {
      this.getCenter(this.currentLocation);
    } else {
      this.getCenter(this.center);
    }
  },
  watch: {
    currentLocation(value) {
      this.getCenter(value);
    },
  },
  computed: {
    ...mapState(["currentLocation"]),
  },
  methods: {
    onFileChange(e) {
      if (!/\.(jpg|jpeg|png|JPG|PNG)$/.test(e.target.value)) {
        alert("The file uploaded need to be -jpeg,jpg,png");
        return false;
      }
      if (
        parseInt(e.target.files.length) > 11 &&
        this.selectedImages.length > 11
      ) {
        alert("You can only upload a maximum of 10 files");
        return false;
      }
      var files = e.target.files;
      files.forEach((file) => {
        file.url = URL.createObjectURL(file);
        this.selectedImages.push(file);
      });
    },
    removeImage(index) {
      this.selectedImages.splice(index, 1);
    },
    getCenter(center) {
      this.center = center;
      this.camera.latitude = center.lat ? center.lat : center[0];
      this.camera.longitude = center.lng ? center.lng : center[1];
      this.getAddress(center);
    },
    getAddress(center) {
      const params = `?format=jsonv2&lat=${
        center.lat ? center.lat : center[0]
      }&lon=${center.lng ? center.lng : center[1]}`;
      axios
        .get("https://nominatim.openstreetmap.org/reverse" + params)
        .then((res) => {
          this.camera.location = res.data.display_name;
        });
    },
    Post() {
      this.isLoading = true;
      const config = {
        headers: { "content-type": "multipart/form-data" },
      };
      let formData = new FormData();
      formData.append("length", this.selectedImages.length);
      this.selectedImages.forEach((data, index) => {
        formData.append("image" + index, data);
      });
      formData.append("camera", JSON.stringify(this.camera));
      axios
        .post("api/camera/", formData, config)
        .then((response) => {
          this.$store.commit("addNewCamera", response.data);
          this.$store.commit("setCenter", [
            response.data.latitude,
            response.data.longitude,
          ]);
          this.isLoading = false;
          this.$emit("completed");
          this.$noti.display(
            "Thank you! You have successfully added new camera.",
            "",
            "normal",
            "success"
          );
        })
        .catch((err) => {
          this.isLoading = false;
          this.$noti.display(err, "", "error", "danger");
        });
    },
  },
};
</script>

<style >
.form-body {
  padding-top: 10px;
}
.file-uploader i {
  font-size: 35px;
  color: rgb(var(--vs-primary));
}
.selected-images img {
  width: 98%;
  height: 100px;
  object-fit: cover;
  margin: auto;
  border-radius: 10px;
}
.file-uploader {
  border-radius: 10px;
  height: 100px;
  width: 98%;
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  border: 2px dashed rgb(var(--vs-primary));
  background-color: rgba(var(--vs-primary), 0.1);
}
.file-uploader p {
  font-size: 12px;
  margin-top: 5px;
  margin-bottom: 0px;
  color: rgb(var(--vs-primary));
}
.remove-image {
  position: absolute;
  right: 10px;
  top: 5px;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 100%;
  color: #fff;
}
</style>