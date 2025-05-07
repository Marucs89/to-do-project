import { ToDos } from "../../../../schemas/to-do";

export default function Modal({ toDo }: { toDo: ToDos[0] }) {
  return (
    <dialog id={`${toDo.todo_id}`}>
      <div>
        <h3>Hello!</h3>
        <p>Press ESC key or click the button below to close</p>
        <div className='modal-action'>
          <form method='dialog'>
            <button className='btn'>Close</button>
          </form>
        </div>
      </div>
    </dialog>
  );
}
