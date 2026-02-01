import { createSlice } from '@reduxjs/toolkit';

const crmSlice = createSlice({
  name: 'crm',
  initialState: {
    messages: [],
    logs: [],
  },
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    setLogs: (state, action) => {
      state.logs = action.payload;
    }
  }
});

export const { addMessage, setLogs } = crmSlice.actions;
export default crmSlice.reducer;