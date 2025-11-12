# Supabase Storage

Complete file storage setup with uploads, downloads, image transformations, and CDN delivery.

## Quick Setup

### 1. Create Storage Bucket

```sql
-- In Supabase Dashboard or SQL Editor
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true);

-- Private bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('documents', 'documents', false);
```

### 2. Set Storage Policies

```sql
-- Public bucket: Anyone can view
CREATE POLICY "Public avatars are accessible"
ON storage.objects FOR SELECT
USING (bucket_id = 'avatars');

-- Authenticated users can upload their own files
CREATE POLICY "Users can upload own avatar"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'avatars' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Users can update their own files
CREATE POLICY "Users can update own avatar"
ON storage.objects FOR UPDATE
TO authenticated
USING (auth.uid()::text = (storage.foldername(name))[1]);

-- Users can delete their own files
CREATE POLICY "Users can delete own avatar"
ON storage.objects FOR DELETE
TO authenticated
USING (auth.uid()::text = (storage.foldername(name))[1]);
```

## File Upload

### Single File Upload (TypeScript)

```typescript
import { supabase } from '@/lib/supabase';

async function uploadFile(file: File, bucket: string = 'avatars') {
  const user = await supabase.auth.getUser();
  if (!user.data.user) throw new Error('Not authenticated');
  
  // Generate unique filename
  const fileExt = file.name.split('.').pop();
  const fileName = `${user.data.user.id}/${Date.now()}.${fileExt}`;
  
  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(fileName, file, {
      cacheControl: '3600',
      upsert: false
    });
  
  if (error) throw error;
  
  // Get public URL
  const { data: { publicUrl } } = supabase.storage
    .from(bucket)
    .getPublicUrl(fileName);
  
  return { path: data.path, url: publicUrl };
}
```

### Upload with Progress

```typescript
async function uploadWithProgress(
  file: File,
  onProgress: (progress: number) => void
) {
  const user = await supabase.auth.getUser();
  if (!user.data.user) throw new Error('Not authenticated');
  
  const fileName = `${user.data.user.id}/${Date.now()}-${file.name}`;
  
  // Split file into chunks for progress tracking
  const chunkSize = 256 * 1024; // 256KB chunks
  const chunks = Math.ceil(file.size / chunkSize);
  
  const { data, error } = await supabase.storage
    .from('uploads')
    .upload(fileName, file, {
      cacheControl: '3600',
      upsert: false
    });
  
  // Note: Native progress not available, use FormData + XMLHttpRequest for real progress
  if (error) throw error;
  
  return data;
}
```

### Multiple Files Upload

```typescript
async function uploadMultiple(files: File[]) {
  const user = await supabase.auth.getUser();
  if (!user.data.user) throw new Error('Not authenticated');
  
  const uploads = files.map(async (file) => {
    const fileName = `${user.data.user.id}/${Date.now()}-${file.name}`;
    
    const { data, error } = await supabase.storage
      .from('uploads')
      .upload(fileName, file);
    
    if (error) throw error;
    
    const { data: { publicUrl } } = supabase.storage
      .from('uploads')
      .getPublicUrl(fileName);
    
    return { path: data.path, url: publicUrl };
  });
  
  return Promise.all(uploads);
}
```

## Image Upload with Compression

```typescript
import imageCompression from 'browser-image-compression';

async function uploadImage(file: File) {
  // Compress image before upload
  const options = {
    maxSizeMB: 1,
    maxWidthOrHeight: 1920,
    useWebWorker: true,
    fileType: 'image/webp' // Convert to WebP
  };
  
  const compressedFile = await imageCompression(file, options);
  
  const user = await supabase.auth.getUser();
  const fileName = `${user.data.user.id}/images/${Date.now()}.webp`;
  
  const { data, error } = await supabase.storage
    .from('images')
    .upload(fileName, compressedFile, {
      contentType: 'image/webp',
      cacheControl: '31536000', // 1 year
      upsert: false
    });
  
  if (error) throw error;
  
  const { data: { publicUrl } } = supabase.storage
    .from('images')
    .getPublicUrl(fileName);
  
  return publicUrl;
}
```

## Image Transformations

### Get Transformed Image URL

```typescript
function getImageUrl(
  path: string,
  options?: {
    width?: number;
    height?: number;
    quality?: number;
    format?: 'webp' | 'jpeg' | 'png';
  }
) {
  const { data } = supabase.storage
    .from('images')
    .getPublicUrl(path, {
      transform: {
        width: options?.width,
        height: options?.height,
        quality: options?.quality || 80,
        format: options?.format || 'webp'
      }
    });
  
  return data.publicUrl;
}

// Usage
const thumbnailUrl = getImageUrl('user/avatar.jpg', {
  width: 200,
  height: 200,
  quality: 85,
  format: 'webp'
});
```

### Common Image Sizes

```typescript
const IMAGE_SIZES = {
  thumbnail: { width: 150, height: 150 },
  small: { width: 400, height: 400 },
  medium: { width: 800, height: 800 },
  large: { width: 1200, height: 1200 },
  og: { width: 1200, height: 630 } // Open Graph
};

function getResponsiveImages(path: string) {
  return {
    thumbnail: getImageUrl(path, IMAGE_SIZES.thumbnail),
    small: getImageUrl(path, IMAGE_SIZES.small),
    medium: getImageUrl(path, IMAGE_SIZES.medium),
    large: getImageUrl(path, IMAGE_SIZES.large),
    original: getImageUrl(path)
  };
}
```

## File Download

### Download File

```typescript
async function downloadFile(path: string, bucket: string = 'documents') {
  const { data, error } = await supabase.storage
    .from(bucket)
    .download(path);
  
  if (error) throw error;
  
  // Create download link
  const url = URL.createObjectURL(data);
  const link = document.createElement('a');
  link.href = url;
  link.download = path.split('/').pop() || 'download';
  link.click();
  
  URL.revokeObjectURL(url);
}
```

### Get Signed URL (Private Files)

```typescript
async function getSignedUrl(path: string, expiresIn: number = 3600) {
  const { data, error } = await supabase.storage
    .from('private-documents')
    .createSignedUrl(path, expiresIn);
  
  if (error) throw error;
  
  return data.signedUrl;
}
```

## File Management

### List Files

```typescript
async function listFiles(folder?: string) {
  const { data, error } = await supabase.storage
    .from('uploads')
    .list(folder, {
      limit: 100,
      offset: 0,
      sortBy: { column: 'created_at', order: 'desc' }
    });
  
  if (error) throw error;
  return data;
}
```

### Delete File

```typescript
async function deleteFile(path: string, bucket: string = 'uploads') {
  const { error } = await supabase.storage
    .from(bucket)
    .remove([path]);
  
  if (error) throw error;
}
```

### Delete Multiple Files

```typescript
async function deleteFiles(paths: string[], bucket: string = 'uploads') {
  const { error } = await supabase.storage
    .from(bucket)
    .remove(paths);
  
  if (error) throw error;
}
```

### Move/Rename File

```typescript
async function moveFile(
  fromPath: string,
  toPath: string,
  bucket: string = 'uploads'
) {
  const { error } = await supabase.storage
    .from(bucket)
    .move(fromPath, toPath);
  
  if (error) throw error;
}
```

## React Components

### File Upload Component

```typescript
'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';

export function FileUpload() {
  const [uploading, setUploading] = useState(false);
  const [url, setUrl] = useState<string | null>(null);

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      const user = await supabase.auth.getUser();
      const fileName = `${user.data.user?.id}/${Date.now()}-${file.name}`;

      const { error } = await supabase.storage
        .from('uploads')
        .upload(fileName, file);

      if (error) throw error;

      const { data } = supabase.storage
        .from('uploads')
        .getPublicUrl(fileName);

      setUrl(data.publicUrl);
    } catch (error) {
      alert('Upload failed!');
    } finally {
      setUploading(false);
    }
  }

  return (
    <div>
      <input
        type="file"
        onChange={handleUpload}
        disabled={uploading}
      />
      {uploading && <p>Uploading...</p>}
      {url && <img src={url} alt="Uploaded" className="mt-4 max-w-xs" />}
    </div>
  );
}
```

### Avatar Upload with Preview

```typescript
'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';
import Image from 'next/image';

export function AvatarUpload({ currentUrl }: { currentUrl?: string }) {
  const [url, setUrl] = useState(currentUrl);
  const [uploading, setUploading] = useState(false);

  async function uploadAvatar(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file');
      return;
    }

    // Validate file size (max 2MB)
    if (file.size > 2 * 1024 * 1024) {
      alert('File size must be less than 2MB');
      return;
    }

    setUploading(true);
    try {
      const user = await supabase.auth.getUser();
      const fileExt = file.name.split('.').pop();
      const fileName = `${user.data.user?.id}/avatar.${fileExt}`;

      const { error } = await supabase.storage
        .from('avatars')
        .upload(fileName, file, { upsert: true });

      if (error) throw error;

      const { data } = supabase.storage
        .from('avatars')
        .getPublicUrl(fileName);

      setUrl(data.publicUrl);

      // Update profile
      await supabase
        .from('profiles')
        .update({ avatar_url: data.publicUrl })
        .eq('id', user.data.user?.id);

    } catch (error) {
      alert('Error uploading avatar');
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="flex items-center gap-4">
      {url && (
        <Image
          src={url}
          alt="Avatar"
          width={100}
          height={100}
          className="rounded-full"
        />
      )}
      <label className="cursor-pointer px-4 py-2 bg-blue-600 text-white rounded-lg">
        {uploading ? 'Uploading...' : 'Upload Avatar'}
        <input
          type="file"
          accept="image/*"
          onChange={uploadAvatar}
          disabled={uploading}
          className="hidden"
        />
      </label>
    </div>
  );
}
```

### Drag & Drop Upload

```typescript
'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';

export function DragDropUpload() {
  const [dragging, setDragging] = useState(false);
  const [files, setFiles] = useState<string[]>([]);

  async function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    
    for (const file of droppedFiles) {
      const user = await supabase.auth.getUser();
      const fileName = `${user.data.user?.id}/${Date.now()}-${file.name}`;

      const { error } = await supabase.storage
        .from('uploads')
        .upload(fileName, file);

      if (!error) {
        const { data } = supabase.storage
          .from('uploads')
          .getPublicUrl(fileName);
        
        setFiles((prev) => [...prev, data.publicUrl]);
      }
    }
  }

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      className={`border-2 border-dashed p-8 rounded-lg ${
        dragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
      }`}
    >
      <p>Drag & drop files here</p>
      <div className="mt-4 grid grid-cols-3 gap-2">
        {files.map((url, i) => (
          <img key={i} src={url} alt="" className="rounded" />
        ))}
      </div>
    </div>
  );
}
```

## Best Practices

### Security
- ✅ Always set RLS policies on storage buckets
- ✅ Validate file types and sizes client-side AND server-side
- ✅ Use folder structure: `userId/filename` for user isolation
- ✅ Never expose service role key client-side
- ✅ Use signed URLs for private files

### Performance
- ✅ Compress images before upload
- ✅ Use WebP format for better compression
- ✅ Leverage CDN caching (cacheControl header)
- ✅ Use image transformations for responsive images
- ✅ Lazy load images with Next.js Image component

### File Naming
- ✅ Use timestamps to prevent overwrites
- ✅ Sanitize filenames (remove special characters)
- ✅ Use consistent folder structure
- ✅ Consider using UUIDs for unique filenames

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-12
