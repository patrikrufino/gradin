<template>
  <div class="bg-gray-100 flex items-center justify-center min-h-screen">
    <div class="max-w-md border rounded-lg overflow-hidden shadow-lg bg-white p-12 flex-col justify-center">
      <img src="/logo-gradin-vertical.png" alt="Logo Gradin" class="mb-12 mx-auto w-32" />
      <form class="grid gap-6" @submit.prevent="submitForm">

        <!-- Dropzone -->
        <div class="flex items-center justify-center w-full">
          <label :class="[
            'flex flex-col items-center justify-center w-64 h-48 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 transition duration-200',
            isHighlighted ? 'border-yellow-500 bg-yellow-100' : 'border-gray-300 bg-gray-50'
          ]" for="dropzone-file" @dragover.prevent="highlight" @dragleave.prevent="removeHighlight"
            @drop.prevent="handleDrop">
            <div class="flex flex-col items-center justify-center pt-5 pb-6">
              <svg v-if="!pdfFile" class="w-8 h-8 mb-4 text-gray-500" aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
              </svg>
              <svg v-else class="w-8 h-8 mb-4 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                viewBox="0 0 24 24">
                <path d="M6 2h9v6h6v14H6V2zm7 2v4h4l-4-4zM7 10h10v2H7v-2zm0 4h10v2H7v-2zm0 4h10v2H7v-2z" />
              </svg>
              <p class="text-sm text-gray-500" v-if="!pdfFile">
                <span class="font-bold">Click para enviar</span> ou arraste e solte</p>
              <p class="text-xs text-gray-500" v-if="!pdfFile">Somente arquivos PDF</p>
              <p v-else class="text-sm font-semibold text-gray-700">{{ pdfFile.name }}</p>
            </div>
            <input ref="fileInput" @change="onFileChange" id="dropzone-file" type="file" class="hidden"
              accept="application/pdf" required />
          </label>
        </div>
        <p v-if="errorMessage" class="text-red-500 text-xs bg-red-100 w-64 text-center py-1 mt-2 border-red-500 rounded-lg transition-opacity duration-1000" :class="{'opacity-100': errorMessage, 'opacity-0': !errorMessage}">{{ errorMessage }}</p>

        <!-- Seletor de Linhas e Colunas -->
        <div class="flex gap-4">
          <div class="w-1/2 flex gap-2 items-center">
            <label for="rows" class="w-3/7 block font-semibold">Linhas</label>

            <select v-model="rows" id="rows" required
              class="cursor-pointer text-center w-4/7 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-yellow-500 focus:border-yellow-500 block p-1">
              <option v-for="n in 6" :key="n" :value="n">{{ n }}</option>
            </select>
          </div>
          <div class="w-1/2 flex gap-2 items-center justify-end">
            <label for="cols" class="w-3/7 block font-semibold">Colunas</label>
            <select v-model="cols" id="cols" required
              class="cursor-pointer text-center w-4/7 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-yellow-500 focus:border-yellow-500 block p-1">
              <option v-for="n in 6" :key="n" :value="n">{{ n }}</option>
            </select>
          </div>
        </div>

        <!-- Botão de Envio -->
        <button type="submit"
          class="font-semibold w-full bg-yellow-400 text-gray-800 py-2 rounded-xl hover:bg-yellow-300 transition duration-200">Gerar
          Gradil</button>
      </form>

      <!-- Link para Download -->
      <div class="flex items-center justify-center">
        <a class="text-center mt-6 font-semibold cursor-pointer no-underline hover:underline text-green-500"
          v-if="downloadUrl" :href="downloadUrl" target="_blank" @click="handleDownload">
          Baixar PDF
        </a>
      </div>
    </div>
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
      isHighlighted: false,
      errorMessage: '', // Adiciona a propriedade para a mensagem de erro
    };
  },
  methods: {
    onFileChange(event: Event) {
      const target = event.target as HTMLInputElement;
      if (target.files) {
        this.setFile(target.files[0]);
      }
    },
    handleDrop(event: DragEvent) {
      event.preventDefault(); // Previne o comportamento padrão
      const files = event.dataTransfer?.files;
      if (files && files.length > 0) {
        this.setFile(files[0]); // Define o arquivo

        // Atualiza o input de arquivo e dispara o evento de mudança
        const fileInput = this.$refs.fileInput as HTMLInputElement;
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(files[0]);
        fileInput.files = dataTransfer.files;

        // Dispara o evento de mudança
        const changeEvent = new Event('change', { bubbles: true });
        fileInput.dispatchEvent(changeEvent);
      }
      this.removeHighlight(); // Garante que o destaque seja removido
    },
    highlight() {
      this.isHighlighted = true;
    },
    removeHighlight() {
      this.isHighlighted = false;
    },
    setFile(file: File) {
      if (file.type === "application/pdf") {
        this.pdfFile = file;
        this.errorMessage = ''; // Limpa a mensagem de erro
      } else {
        this.errorMessage = "Arquivo inválido! Apenas PDFs são permitidos.";
        setTimeout(() => {
          this.errorMessage = '';
        }, 5000);
      }
    },
    async submitForm() {
      if (!this.pdfFile) {
        alert("Nenhum arquivo PDF selecionado.");
        return;
      }

      const formData = new FormData();
      formData.append('pdf_file', this.pdfFile);
      formData.append('rows', this.rows.toString());
      formData.append('cols', this.cols.toString());

      try {
        console.log("Enviando formulário...");
        const response = await this.$axios.$post('make_poster/', formData);
        console.log("Resposta recebida:", response);
        this.downloadUrl = response.download_url;
      } catch (error) {
        console.error('Erro ao enviar o formulário:', error);
        if (error.response) {
          console.error('Resposta do servidor:', error.response);
        }
      }
    },

    handleDownload() {
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    },
  },
});
</script>
