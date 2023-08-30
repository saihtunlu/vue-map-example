<template>
  <div class="row">
    <div class="col-12 form-body">
      <div class="row">
        <div class="col-12">
          <label class="custom-label mb-0">Note</label>
          <textarea class="custom-textarea" v-model="activity.note"></textarea>
        </div>
        <div class="col-12">
          <vs-select label="Camera Status" v-model="activity.cameraStatus">
            <vs-option label="Good" value="Good"> Good </vs-option>
            <vs-option label="Disabled" value="Disabled"> Disabled </vs-option>
          </vs-select>
        </div>
        <div class="col-12">
          <label style="font-size: 0.75rem; padding-left: 10px">Media</label>
        </div>
        <div class="col-12">
          <div class="row mx-0">
            <div class="col-12 px-0 mb-2 selected-images" v-if="selectedImage">
              <span class="remove-image" @click="removeImage()"
                ><i class="bx bx-x"></i
              ></span>
              <img
                :src="selectedImage.url"
                style="height: 150px !important; width: 100% !important"
                alt=""
              />
            </div>
            <div class="col-12 pointer mb-2 px-0" v-if="!selectedImage">
              <input
                type="file"
                ref="fileInput"
                hidden
                class="uploader pointer"
                @change="onFileChange"
                name=""
              />
              <div
                class="file-uploader"
                style="height: 150px !important; width: 100% !important"
                @click="$refs.fileInput.click()"
              >
                <i class="bx bx-camera"></i>
                <p>Add Image</p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-12 bottom-btn">
          <vs-button class="w-100" size="large" flat @click="$emit('cancel')"
            >Cancel
          </vs-button>
          <vs-button
            class="w-100 ml-2"
            size="large"
            :loading="isLoading"
            @click="Post"
            >Update
          </vs-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// import { mapState } from "vuex";
export default {
  props: {
    camera: {},
  },
  data() {
    return {
      selectedImage: null,
      isLoading: false,
      activity: {
        camera: null,
        note: null,
        time: null,
        cameraStatus: "Good",
      },
    };
  },
  components: {},
  mounted() {
    this.activity.camera = this.camera.id;
    this.activity.cameraStatus = this.camera.status;
  },
  watch: {},
  computed: {},
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
      var file = e.target.files[0];
      file.url = URL.createObjectURL(file);
      this.selectedImage = file;
    },
    removeImage() {
      this.selectedImage = null;
    },
    Post() {
      this.isLoading = true;
      const config = {
        headers: { "content-type": "multipart/form-data" },
      };
      let formData = new FormData();
      if (this.selectedImage) {
        formData.append("image", this.selectedImage);
      }
      formData.append("activity", JSON.stringify(this.activity));
      axios
        .post("api/activities/", formData, config)
        .then((response) => {
          this.isLoading = false;
          this.$emit("completed", response.data);
          this.$noti.display(
            "Thank you! You have successfully updated the camera.",
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

<style scoped>
</style>