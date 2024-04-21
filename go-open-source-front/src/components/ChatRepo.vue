<template>
    <div class="page-container">
      <!-- Левая колонка с буллет-поинтами -->
      <div class="sidebar">
      <div class="content-wrapper">
        <h1>Кофе Магазин</h1>
        <hr class="divider" /> <!-- Разделительная линия -->
        <div class="buttons-wrapper">
          <button class="sidebar-button">master</button>
          <button class="sidebar-button">ветки: 9</button>
        </div>
        <div class="icon-wrapper">
        <h3 style="margin-bottom: 5px;">Контрибьюторы</h3>
          <div class="icon-item">
            <div class="circle-icon" style="background-color: #0AD5C1;"></div>
            <span>venikhl</span>
          </div>
          <div class="icon-item">
            <div class="circle-icon" style="background-color: #0EC879;"></div>
            <span>Ninel</span>
          </div>
          <!-- Добавьте другие иконки здесь -->
        </div>
        <div class="description-container">
          <div class="top-section">
            <!-- <img :src="bookUrl" alt="Book Icon" class="book-icon" /> -->

            <span>README</span>
          </div>
          <hr class="description-divider" /> 
          <div class="bottom-section">
            <!-- Здесь может быть другое содержимое -->

          </div>
        </div>
        <p>Количество звезд: 100</p>
        <p>Последний коммит: 2024-04-20</p>
       
      </div>
    </div>
  
      <!-- Правая колонка с чатом -->
      <div class="wrapper">
        
      <header class="chat-header">ЧатБот</header>
        <div class="chat-container">
          <ul class="chat-thread">
            <li v-for="(message, index) in messages" :key="index" :class="message.author === 'user' ? 'user-message' : 'bot-message'">
              <div class="message-container">
                <div class="avatar" :class="message.author === 'user' ? 'user-avatar' : 'bot-avatar'"></div>
                <div class="message-content">{{ message.text }}</div>
              </div>
            </li>
          </ul>
  
          <form class="chat-window" @submit.prevent="sendMessage">
            <input ref="messageInput" class="chat-window-message" type="text" v-model="newMessage" autocomplete="off" autofocus />
          </form>
        </div>
      </div>
    </div>
  </template>
  
  
  <script>
  import router from "@/router";
  import bookImg from "@/assets/img/book.png";
  export default {
    data() {
      return {
        
        bookUrl: bookImg,
        messages: [
          { text: 'Привет! Что ты хочешь узнать?', author: 'bot' },
          { text: 'Я здесь, чтобы помочь. Задавайте вопросы!', author: 'bot' }
        ],
        newMessage: '',
        sendChannel: null,
        receiveChannel: null
      };
    },
    mounted() {
      this.createConnection();
    },
    methods: {
      async createConnection() {
        const servers = null;
        this.localPeerConnection = new RTCPeerConnection(servers);
        this.localPeerConnection.onicecandidate = this.gotLocalCandidate;
  
        this.sendChannel = this.localPeerConnection.createDataChannel('sendDataChannel', { reliable: false });
        this.sendChannel.onopen = this.handleSendChannelStateChange;
        this.sendChannel.onclose = this.handleSendChannelStateChange;
  
        const desc = await this.localPeerConnection.createOffer();
        await this.gotLocalDescription(desc);
      },
      async gotLocalDescription(desc) {
        await this.localPeerConnection.setLocalDescription(desc);
        this.remotePeerConnection = new RTCPeerConnection(null);
        this.remotePeerConnection.onicecandidate = this.gotRemoteIceCandidate;
        this.remotePeerConnection.ondatachannel = this.gotReceiveChannel;
  
        await this.remotePeerConnection.setRemoteDescription(desc);
        const answerDesc = await this.remotePeerConnection.createAnswer();
        await this.gotRemoteDescription(answerDesc);
      },
      async gotRemoteDescription(desc) {
        await this.remotePeerConnection.setLocalDescription(desc);
        await this.localPeerConnection.setRemoteDescription(desc);
      },
      gotLocalCandidate(event) {
        if (event.candidate) {
          this.remotePeerConnection.addIceCandidate(event.candidate);
        }
      },
      gotRemoteIceCandidate(event) {
        if (event.candidate) {
          this.localPeerConnection.addIceCandidate(event.candidate);
        }
      },
      gotReceiveChannel(event) {
        this.receiveChannel = event.channel;
        this.receiveChannel.onmessage = this.handleMessage;
      },
      async handleMessage(event) {
        this.messages.push({ text: event.data, author: 'bot' });
      },
      async handleSendChannelStateChange() {
        if (this.$refs.messageInput && this.sendChannel.readyState === 'open') {
          this.$refs.messageInput.disabled = false;
          this.$refs.messageInput.focus();
        } else if (this.$refs.messageInput) {
          this.$refs.messageInput.disabled = true;
        }
      },
      async sendMessage() {
        if (this.sendChannel.readyState === 'open' && this.newMessage.trim() !== '') {
          this.sendChannel.send(this.newMessage.trim());
          this.messages.push({ text: this.newMessage.trim(), author: 'user' });
          this.newMessage = '';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .page-container {
  display: flex;
  flex-direction: column; /* Ensure children stack vertically */
  min-height: 100vh; /* Minimum height of page container is full viewport height */
}
.description-container {
  background-color: #161b22;
  border: 1px solid #fff;
  width: 59.7vw;
  height: 30vh;
  /* padding: 10px; */
  box-sizing: border-box;
  margin-top: 10px;
  border-radius: 10px;
  border-bottom: 1px solid #fff; /* Установка border-bottom */
}

.description-divider {
  border: none;
  border-top: 1px solid white;
  width: 100%;
  margin: 3px 0;
}


/* Стили для верхней части блока */
.top-section {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 20%; /* Высота верхней части (20% от общей высоты блока) */
  padding: 5px 5px 0px 15px;
}

.book-icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

/* Стили для нижней части блока */
.bottom-section {
  height: 80%; /* Высота нижней части (80% от общей высоты блока) */
  /* Дополнительные стили по вашему усмотрению */
}
  /* Стили для под-дива с иконками */
.icon-wrapper {
  background-color: #28303a; /* Цвет фона под-дива */
  border-radius: 10px;
  border: 1px solid #727981; /* Окантовка под-дива */
  padding: 10px; /* Внутренние отступы */
  margin-top: 20px; /* Отступ сверху */
}

/* Стили для элементов внутри иконки */
.icon-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px; /* Отступ между элементами */
}

/* Стили для круглой иконки */
.circle-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: 10px;
}

/* Стили для текста рядом с иконкой */
.icon-item span {
  color: white; /* Цвет текста */
}

.sidebar {
  width: 68.9vw; /* Ширина левой колонки */
  padding: 20px;
  background-color: #161b22; /* Черный фон */
  height: 100vh; /* Занимает всю высоту окна просмотра */
  box-sizing: border-box; /* Учитываем padding внутри ширины и высоты */
  display: flex;
  flex-direction: column;
}

.content-wrapper {
  text-align: left; /* Выравнивание текста по левой стороне */
  max-width: 90%; /* Максимальная ширина содержимого */
  color: white; /* Белый цвет текста */
}

.content-wrapper h2,
.content-wrapper p {
  font-size: 20px;
  margin: 10px 0; /* Отступы между заголовками и параграфами */
}

.divider {
  border-top: 1px solid white; /* Белая разделительная линия */
  margin-bottom: 15px; /* Отступ после линии */
}

.buttons-wrapper {
  display: flex;
  justify-content: space-between;
}
.buttons-wrapper button {
  flex-grow: 1; /* Равномерное распределение доступного пространства */
  margin-right: 5px; /* Минимальный отступ между кнопками */
}
.sidebar-button {
  padding: 8px 16px;
  background-color: #28303a; /* Цвет кнопок, похожий на GitHub */
  color: white;
  border: none;
  border-radius: 4px;
  border-color: #727981;
  cursor: pointer;
  font-size: 14px;
}

.sidebar-button:hover {
  background-color: #9fb2ca; /* Цвет при наведении */
  color: #161b22;
}
.chat-header {
  font-size: 24px; /* Размер шрифта заголовка */
  color: white; /* Цвет текста заголовка */
  text-align: center; /* Выравнивание текста по центру */
  padding: 10px 0; /* Внутренние отступы сверху и снизу */
  background-color: #404a5a; /* Цвет фона заголовка */
  border-bottom: 1px solid #28303a; /* Линия под заголовком */
  border-radius: 8px; /* Скругление углов сверху слева и справа */
  margin-bottom: 5vh;
}
  
  /* Стили для внешнего контейнера чата */
  .wrapper {
    background-color:#161b22;
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: calc(100vw - 70vw); /* Оставшаяся ширина после вычета ширины левой колонки */
    display: flex;
    flex-direction: column;
    justify-content: space-between; /* Распределение контента внутри контейнера */
    padding: 20px; /* Отступы вокруг контейнера */
    box-sizing: border-box; /* Учитываем padding внутри ширины и высоты */
  }
  
  /* Остальные стили чата (уже определены ранее) */
  .chat-container {
    flex: 1;
    overflow-y: auto;
  }
  /* Стили для списка сообщений */
  .chat-thread {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  /* Стили для контейнера каждого сообщения */
  .message-container {
    display: flex;
    align-items: flex-start;
    margin-bottom: 12px; /* Отступ между сообщениями */
  }

  /* Стили для аватара */
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #ccc; /* Цвет аватара (замените на изображение, если нужно) */
    margin-right: 10px;
  }

  /* Стили для аватара пользователя */
  .user-avatar {
    background-color: #0AD5C1; /* Цвет аватара пользователя */
  }

  /* Стили для аватара бота */
  .bot-avatar {
    background-color: #0EC879; /* Цвет аватара бота */
  }

  /* Стили для содержимого сообщения */
  .message-content {
    padding: 10px;
    border-radius: 10px;
    background-color: #ffffff; /* Цвет фона сообщения */
    font-size: 16px;
    max-width: 70%; /* Максимальная ширина текста сообщения */
    word-wrap: break-word; /* Перенос длинных слов */
  }

  /* Стили для сообщения пользователя (справа) */
  .user-message .message-container {
    justify-content: flex-end; /* Выравнивание сообщений пользователя справа */
  }

  /* Стили для сообщения бота (слева) */
  .bot-message .message-container {
    justify-content: flex-start; /* Выравнивание сообщений бота слева */
  }

  /* Стили для формы ввода сообщения */
  .chat-window {
    margin-top: 20px; /* Отступ от верхней границы области чата */
  }

  /* Стили для поля ввода сообщения */
  .chat-window-message {
    width: 100%;
    height: 48px;
    font: 16px 'Noto Sans', sans-serif;
    background: none;
    color: #ffffff;
    border: 0;
    border: 2px solid rgb(255, 255, 255);
    border-radius: 10px;
    outline: none;
    padding: 10px; /* Внутренние отступы вокруг текстового поля */
    box-sizing: border-box; /* Учитываем padding внутри ширины */
  }
</style>
