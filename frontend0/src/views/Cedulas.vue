<template>
    
  <v-data-table :headers="headers" :items="cedulas" sort-by="ID_cedula" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat>
      <v-toolbar-title class="subheading blue--text">CEDULAS DE VOTACIÓN</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>

        <v-dialog v-model="dialog" max-width="500px">

          <v-card>
            <v-card-title>
              <span class="text-h5 blue--text">{{ formCedula }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.ID_elector"
                      label="ID del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.DNI_elector"
                      label="DNI del elector"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Nombre_elector"
                      label="Nombre del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Apellidos_elector"
                      label="Apellido del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Estado_elector"
                      label="Estado del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Tipo_elector"
                      label="Tipo de elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Direccion_elector"
                      label="Dirección del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Departamento_elector"
                      label="Departamento del elector"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Email_elector"
                      label="Email del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Telefono_elector"
                      label="Teléfono del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Nacimiento_elector"
                      label="Fecha de nacimiento del elector"
                      hint="YYYY/MM/DD format"
                      persistent 
                      prepend-icon="event" 
                      @blur="date = parseDate(dateFormatted)" 
                      v-on="on">
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Genero_elector"
                      label="Género del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Password_elector"
                      label="Password del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.ID_ubigeo_elector"
                      label="Ubigeo del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.vector_elector"
                      label="Vector de reconocimiento del elector"
                    ></v-text-field>
                  </v-col>

                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn color="red darken-1" text @click="close">
                Cancelar
              </v-btn>

              <v-btn color="green darken-1" text @click="save">
                Guardar
              </v-btn>

            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">¿Estas seguro de eliminar este item?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="red darken-1" text @click="closeDelete">Cancelar</v-btn>
              <v-btn color="green darken-1" text @click="deleteItemConfirm">Confirmar</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>

    </template>
  
    <template v-slot:no-data>
      <v-btn
        color="primary"
        @click="initialize"
      >
        Actualizar
      </v-btn>
    </template>

  </v-data-table>
</template>

<script>
  import axios from 'axios';
  var url = 'http://127.0.0.1:5000/cedula';
  export default {
    data: () => ({
      config_request: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
      },          
      dialog: false,
      dialogDelete: false,
      headers: [
        { text: 'ID', value: 'ID_cedula' },
        { text: 'Partido Político', value: 'ID_partido_politico_cedula' },
        { text: 'Candidato', value: 'ID_candidato_cedula' },
        { text: 'Código Ubigeo', value: 'ID_ubigeo_cedula' },
        { text: 'Fecha de emisión', value: 'Fecha_cedula_voto' },
        { text: 'Elección', value: 'ID_eleccion' },
        { text: 'ID del elector', value: 'ID_elector_cedula' },
      ],
      cedulas: [],
      editedIndex: -1,
      editedItem: {
        ID_cedula: '',
        ID_elector_cedula: '',
        ID_partido_politico_cedula: '',
        ID_candidato_cedula: '',
        ID_ubigeo_cedula: '',
        Fecha_cedula_voto: '',
        ID_eleccion: '',
      },
      defaultItem: {
        ID_cedula: '',
        ID_elector_cedula: '',
        ID_partido_politico_cedula: '',
        ID_candidato_cedula: '',
        ID_ubigeo_cedula: '',
        Fecha_cedula_voto: '',
        ID_eleccion: '',
      },
    }),

    computed: {
      formCedula () {
        return this.editedIndex === -1 ? 'Nueva cedula' : 'Editar cedula'
      },
    },

    watch: {
      dialog (val) {
        val || this.close()
      },
      dialogDelete (val) {
        val || this.closeDelete()
      },
    },

    created () {
      // this.initialize()
      this.getItems()
    },

    methods: {
      initialize () {
        this.cedulas = [
            {
            ID_elector : "sha45ty929",
            DNI_elector : 76918799,
            Nombre_elector : "Fabricio",
            Apellidos_elector : "Centeno",
            Estado_elector : "0",
            Tipo_elector : "elector",
            Direccion_elector : "Urb. Crisantemos",
            Departamento_elector : "Arequipa",
            Email_elector : "rcentenoc@gmail.com",
            Telefono_elector : "989131389",
            Nacimiento_elector : "1997-10-28",
            Genero_elector : "Masculino",
            Password_elector : "4587541213",
            ID_ubigeo_elector : "040101",
            vector_elector :"0.154632"
          },
        ]
      },

      getItems () {
        axios.get(url, {
          headers: this.config_request
        })
        .then(response => {
          this.cedulas = response.data
        })
        .catch(error => {
          console.log(error)
        })
      },

      actionEdit (item) {
        this.editedIndex = this.cedulas.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.cedulas.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        axios.delete(url + '/' + this.editedItem.ID_elector, {
          headers: this.config_request
        })
        .then(response => {
          this.getItems()
          this.closeDelete()
        })
        .catch(error => {
          console.log(error)
        })
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      addItem () {
        axios.post(url+'/nuevo', this.editedItem, {
          headers: this.config_request
        })
        .then(response => {
          this.cedulas.push(response.data)
          this.close()
        })
        .catch(error => {
          console.log(error)
        })
        // this.cedulas.push(this.editedItem)
      },

      editItem (){
        axios.put(url+'/editar/'+this.editedItem.ID_elector, this.editedItem, {
          headers: this.config_request
        })
        .then(response => {
          this.getItems()
          this.close()
        })
        .catch(error => {
          console.log(error)
        })
      },

      save () {
        if (this.editedIndex > -1) {
          console.log("editar")
          this.editItem()
          // Object.assign(this.cedulas[this.editedIndex], this.editedItem)
        } else {
          console.log("crear")
          this.addItem()
          // this.cedulas.push(this.editedItem)
        }
        this.close()
      },

      parseDate(date){
        if(!date) return null
        const [day, month, year] = date.split('/');
        return `${day.padStart(2,'0')}-${month.padStart(2,'0')}-${year}`;
      },
    },
  }
</script>


