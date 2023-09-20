import { create } from "zustand";
import backend from "./api";

const useStore = create((set) => ({
	login: null,
	setLogin: (newState) => set({ login: newState }),
}));

export default useStore;
