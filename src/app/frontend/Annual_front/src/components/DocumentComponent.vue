<template>
  <q-page>
    <div class="q-pa-md">
      <q-card flat bordered class="doc-card">
        <q-card-section>
          <div class="text-h6 text-center animated fadeIn">Gestion des Documents</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit.prevent="addDocument">
            <q-input
              v-model="documentTitle"
              label="Titre du document"
              outlined
              dense
              clearable
              :error="!!errors.title"
              :error-message="errors.title"
              class="input-field neon-input"
            />

            <!-- Upload des docs -->
            <q-file
              v-model="documentFile"
              label="Ajouter un fichier"
              filled
              bottom-slots
              counter
              max-files="1"
              :error="!!errors.file"
              :error-message="errors.file"
              class="input-field neon-input"
            >
              <template v-slot:before>
                <q-icon name="folder_open" />
              </template>
              <template v-slot:hint>
                Sélectionnez un fichier
              </template>
            </q-file>

            <q-btn
              type="submit"
              label="Sauvegarder"
              class="submit-btn neon-btn full-width"
            />
          </q-form>
        </q-card-section>

        <q-card-section>
          <q-list bordered class="q-mt-md">
            <q-item
              v-for="(doc, index) in documents"
              :key="index"
              class="q-items-between"
            >
              <q-item-section>
                <span><b>{{ doc.title }}</b></span>
              </q-item-section>
              <q-item-section side>
                <q-btn
                  flat
                  round
                  dense
                  icon="link"
                  label="Télécharger"
                  @click="downloadFile(doc.file)"
                  class="action-btn neon-btn"
                />
              </q-item-section>
              <q-item-section side>
                <q-btn
                  flat
                  round
                  dense
                  icon="delete"
                  color="negative"
                  @click="removeDocument(index)"
                  class="action-btn neon-btn"
                />
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'DocumentComponent',
  setup() {
    const documents = ref([]); // Liste des documents ajoutés
    const documentTitle = ref(''); // Titre du document
    const documentFile = ref(null); // Fichier sélectionné
    const errors = ref({ title: '', file: '' }); // Gestion des erreurs

    const addDocument = () => {
      // Réinitialisation des erreurs
      errors.value.title = '';
      errors.value.file = '';

      // Validation
      if (!documentTitle.value.trim()) {
        errors.value.title = 'Le titre est requis.';
      }

      if (!documentFile.value || !(documentFile.value instanceof File)) {
        errors.value.file = 'Un fichier valide est requis.';
      }

      // Si pas d'erreurs, ajouter le document
      if (!errors.value.title && !errors.value.file) {
        documents.value.push({
          title: documentTitle.value.trim(),
          file: documentFile.value,
        });

        // Réinitialisation des champs
        documentTitle.value = '';
        documentFile.value = null;
      }
    };

    const removeDocument = (index) => {
      documents.value.splice(index, 1);
    };

    const downloadFile = (file) => {
      if (!file || !(file instanceof File)) {
        console.error('Fichier invalide ou inexistant.');
        return;
      }

      const url = URL.createObjectURL(file);
      const link = document.createElement('a');
      link.href = url;
      link.download = file.name || 'document';
      link.click();

      URL.revokeObjectURL(url);
    };

    return {
      documents,
      documentTitle,
      documentFile,
      errors,
      addDocument,
      downloadFile,
      removeDocument,
    };
  },
};
</script>

<style scoped>
.q-page {
  background: linear-gradient(135deg, #121212, #1e1e2f);
  color: #e0e0e0;
}

.doc-card {
  background: linear-gradient(145deg, #33334d, #4f4f72);
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7), 0 0 20px rgba(221, 115, 15, 0.5);
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  overflow: hidden;
}

/* En-tête */
.text-h6 {
  font-weight: 600;
  color: #fff;
  margin-bottom: 20px;
  text-shadow: 0 0 15px #d47f00, 0 0 20px #00bcd4;
}

/* Champs de saisie et fichiers */
.input-field,
.neon-input:focus-within {
  border-color: #d47f00;
  color: #fff !important;
  transition: all 0.3s ease;
}

/* Bouton de sauvegarde */
.submit-btn {
  margin-top: 30px;
  background-color: #d47f00;
  color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px #d47f00, 0 0 10px #d47f00;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: scale(1.05);
  background-color: #d47f00;
  box-shadow: 0 4px 15px rgba(221, 115, 15, 0.5);
}

/* Boutons d'action */
.action-btn {
  transition: color 0.3s ease;
}

.action-btn:hover {
  color: #d47f00;
  text-shadow: 0 0 10px #d47f00, 0 0 20px #d47f00;
}

/* Liste des documents */
.q-list {
  max-height: 300px;
  overflow-y: auto;
}

.q-item {
  transition: background-color 0.3s ease;
}

.q-item:hover {
  background-color: #f1f1f1;
}

/* Animation de fade-in */
.animated {
  animation-duration: 0.5s;
  animation-timing-function: ease-out;
}

.fadeIn {
  animation-name: fadeIn;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
