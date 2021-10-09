<template>
  <div>
    <!-- 一般設定 -->
    <v-card outlined class="mb-4 pa-2">
      <v-list two-line subheader>
        <v-subheader>
          <v-icon small class="mr-2">mdi-cog</v-icon> 一般
        </v-subheader>

        <v-list-item @click="limitDialog = true">
          <v-list-item-content>
            <v-list-item-title>表示数</v-list-item-title>
            <v-list-item-subtitle
              >今日のタスク一覧の表示数を変更
            </v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action>{{ formatLimit }}</v-list-item-action>
          <v-dialog v-model="limitDialog" max-width="300">
            <v-card>
              <v-list dense>
                <v-list-item
                  v-for="limit in limits"
                  @click="updateLimit(limit)"
                >
                  <v-list-item-content>
                    <v-list-item-title>{{ limit }} 件</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item @click="updateLimit('all')">
                  <v-list-item-content>
                    <v-list-item-title>すべて</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-dialog>
        </v-list-item>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>通知</v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-switch
              v-model="notice.is_notification"
              @click="updateNotice"
              inset
            ></v-switch>
          </v-list-item-action>
        </v-list-item>

        <TimeSelect
          v-model="notice.time"
          @save="updateNotice"
          v-if="notice.is_notification"
        >
          <template #activator="{ on }">
            <v-list-item v-on="on">
              <v-list-item-content>
                <v-list-item-title>通知時間</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>{{ notice.time }}</v-list-item-action>
            </v-list-item>
          </template>
        </TimeSelect>
      </v-list>
    </v-card>

    <!-- アカウント設定 -->
    <v-card outlined class="mb-4 pa-2">
      <v-list subheader>
        <v-subheader>
          <v-icon small class="mr-2">mdi-account-circle</v-icon> アカウント
        </v-subheader>

        <v-list-item to="/setting/email">
          <v-list-item-content>
            <v-list-item-title>メールアドレスの変更</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/setting/password">
          <v-list-item-content>
            <v-list-item-title>パスワードの変更</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click="logoutDialog = true">
          <v-list-item-content>
            <v-list-item-title>ログアウト</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-dialog v-model="logoutDialog" max-width="300">
          <v-card>
            <div class="pa-4">ログアウトしますか</div>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="logoutDialog = false">キャンセル</v-btn>
              <v-btn depressed class="primary" to="/sign_out">
                ログアウト
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-list>
    </v-card>

    <!-- アプリについて -->
    <v-card outlined class="mb-4 pa-2">
      <v-list subheader>
        <v-subheader>
          <v-icon small class="mr-2">mdi-information</v-icon> アプリについて
        </v-subheader>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>バージョン</v-list-item-title>
          </v-list-item-content>
          <v-list-item-action> 0.0.1 </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      header: {
        title: '設定',
      },
      limitDialog: false,
      logoutDialog: false,
      limits: [5, 10, 15, 20],
      limit: null,
      notice: {
        is_notification: false,
        time: '8:00',
      },
    }
  },
  computed: {
    formatLimit() {
      if (typeof this.limit === 'number') {
        return this.limit + '件'
      } else {
        return 'すべて'
      }
    },
  },
  mounted() {
    this.updateHeader()
  },
  methods: {
    updateHeader() {
      // タイトルとして使いたい情報を渡す
      this.$nuxt.$emit('updateHeader', this.header.title)
    },
    // 通知設定の更新
    updateNotice() {
      console.log(this.is_notification)
      this.$axios
        .put('/api/setting/notification', this.notice)
        .then(console.log('更新'))
        .catch((error) => {})
    },
    // 表示件数の更新
    updateLimit(limit) {
      this.limit = limit
      this.limitDialog = false
      this.$axios
        .put('/api/setting/limit', { limit: this.limit })
        .then(console.log('更新'))
        .catch((error) => {})
    },
  },
}
</script>
