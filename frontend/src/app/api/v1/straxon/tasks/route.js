import { NextResponse } from 'next/server';
import { createUserTask } from '@/lib/db';

// POST /api/v1/straxon/tasks
// Kullanıcı için yeni görev oluştur
export async function POST(request) {
  try {
    const { profile_id, task_type, title, description, metadata } = await request.json();

    if (!profile_id || !title) {
      return NextResponse.json(
        { error: 'profile_id ve title zorunludur' },
        { status: 400 }
      );
    }

    const task = await createUserTask(profile_id, task_type, title, description, metadata);
    return NextResponse.json({ status: 'created', task });
  } catch (err) {
    console.error('Task create error:', err);
    return NextResponse.json(
      { error: 'Sunucu hatası', detail: err.message },
      { status: 500 }
    );
  }
}
