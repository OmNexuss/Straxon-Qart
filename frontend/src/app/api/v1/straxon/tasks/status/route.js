import { NextResponse } from 'next/server';
import { updateTaskStatus } from '@/lib/db';

// PATCH /api/v1/straxon/tasks/status
// Görev tamamlama durumunu güncelle
export async function PATCH(request) {
  try {
    const { task_id, is_completed } = await request.json();

    if (!task_id || is_completed === undefined) {
      return NextResponse.json(
        { error: 'task_id ve is_completed zorunludur' },
        { status: 400 }
      );
    }

    const updated = await updateTaskStatus(task_id, is_completed);
    return NextResponse.json({ status: 'updated', task: updated });
  } catch (err) {
    console.error('Task status update error:', err);
    return NextResponse.json(
      { error: 'Sunucu hatası', detail: err.message },
      { status: 500 }
    );
  }
}
