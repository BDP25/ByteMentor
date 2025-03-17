// Um sicherzustellen, dass alle Nachtichtenobjekte einem Aufbau folgen
export interface Message {
  text: string;
  sender: "user" | "bot";
}
