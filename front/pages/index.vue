<template>
  <div>
    <h1>Gerador de Gradil</h1>
    <form @submit.prevent="submitForm">
      <input type="file" @change="onFileChange" required />
      <input type="number" v-model="rows" required placeholder="Número de linhas" />
      <input type="number" v-model="cols" required placeholder="Número de colunas" />
      <button type="submit">Gerar Gradil</button>
    </form>
    <a v-if="downloadUrl" :href="downloadUrl" download>Baixar PDF</a>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      pdfFile: null as File | null,
      rows: 1,
      cols: 1,
      downloadUrl: null as string | null,
    };
  },
  methods: {
    onFileChange(event: Event) {
      const target = event.target as HTMLInputElement;
      if (target.files) {
        this.pdfFile = target.files[0];
      }
    },
    async submitForm() {
      if (!this.pdfFile) return;

      const formData = new FormData();
      formData.append('pdf_file', this.pdfFile);
      formData.append('rows', this.rows.toString());
      formData.append('cols', this.cols.toString());

      try {
        const response = await this.$axios.$post('make_poster/', formData);
        this.downloadUrl = response.download_url; // Certifique-se de que isso está correto
      } catch (error) {
        console.error('Erro ao enviar o formulário:', error);
      }
    },
  },
});
</script>
